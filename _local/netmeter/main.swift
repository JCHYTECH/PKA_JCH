import Cocoa
import Darwin

// NetMeter — débit ↓/↑ + état de la connexion dans la barre de menu macOS.
// - Débit temps réel : compteurs if_data des interfaces "en*", chaque seconde.
// - Latence continue : ping ICMP toutes les 30 s → point coloré vivant.
// - Test complet : networkQuality (débit + réactivité) → verdict qualitatif.

struct NetCounters {
    var inBytes: UInt64 = 0
    var outBytes: UInt64 = 0
    var ip: String = "—"
    var iface: String = "—"
}

func readCounters() -> NetCounters {
    var c = NetCounters()
    var ifaddrPtr: UnsafeMutablePointer<ifaddrs>? = nil
    guard getifaddrs(&ifaddrPtr) == 0, let first = ifaddrPtr else { return c }
    defer { freeifaddrs(ifaddrPtr) }

    var ptr: UnsafeMutablePointer<ifaddrs>? = first
    while let ifa = ptr {
        let name = String(cString: ifa.pointee.ifa_name)
        let flags = Int32(ifa.pointee.ifa_flags)
        let isUp = (flags & IFF_UP) != 0
        let isRunning = (flags & IFF_RUNNING) != 0
        let isLoopback = (flags & IFF_LOOPBACK) != 0

        // Interfaces physiques Wi-Fi/Ethernet uniquement (exclut awdl0, llw0, bridge0, utun*…)
        if name.hasPrefix("en") && isUp && isRunning && !isLoopback {
            if c.iface == "—" { c.iface = name }
            guard let addr = ifa.pointee.ifa_addr else {
                ptr = ifa.pointee.ifa_next
                continue
            }
            switch addr.pointee.sa_family {
            case UInt8(AF_LINK):
                if let raw = ifa.pointee.ifa_data {
                    let d = raw.assumingMemoryBound(to: if_data.self).pointee
                    c.inBytes += UInt64(d.ifi_ibytes)
                    c.outBytes += UInt64(d.ifi_obytes)
                }
            case UInt8(AF_INET):
                let sin = addr.withMemoryRebound(to: sockaddr_in.self, capacity: 1) { $0.pointee }
                var a = sin.sin_addr
                var buf = [CChar](repeating: 0, count: Int(INET_ADDRSTRLEN))
                inet_ntop(AF_INET, &a, &buf, socklen_t(buf.count))
                let s = String(cString: buf)
                if s != "0.0.0.0" && !s.hasPrefix("169.254") { c.ip = s }
            default:
                break
            }
        }
        ptr = ifa.pointee.ifa_next
    }
    return c
}

func fmtCompact(_ b: Double) -> String {
    let v = max(0, b)
    if v >= 1_000_000_000 { return String(format: "%.1fG", v / 1_000_000_000) }
    if v >= 1_000_000 { return String(format: "%.1fM", v / 1_000_000) }
    if v >= 1_000 { return String(format: "%.0fK", v / 1_000) }
    return String(format: "%.0fB", v)
}

func fmtFull(_ b: Double) -> String {
    let v = max(0, b)
    if v >= 1_000_000_000 { return String(format: "%.1f GB/s", v / 1_000_000_000) }
    if v >= 1_000_000 { return String(format: "%.1f MB/s", v / 1_000_000) }
    if v >= 1_000 { return String(format: "%.0f KB/s", v / 1_000) }
    return String(format: "%.0f B/s", v)
}

func firstMatch(_ pattern: String, in text: String) -> String? {
    guard let re = try? NSRegularExpression(pattern: pattern) else { return nil }
    let nsRange = NSRange(text.startIndex..., in: text)
    guard let m = re.firstMatch(in: text, range: nsRange),
          let r = Range(m.range(at: 1), in: text) else { return nil }
    return String(text[r])
}

// MARK: - Analyse qualitative du test networkQuality

struct QualityReport {
    var downlink: Double?
    var uplink: Double?
    var responsiveness: String?
    var idleLatencyMs: Double?
    var verdict: String = "Indéterminée"
    var emoji: String = "⚪️"

    func explanation() -> String {
        switch verdict {
        case "Excellente": return "Ligne réactive et rapide — aucun problème détecté."
        case "Bonne": return "Connexion saine — réserves mineures seulement."
        case "Moyenne": return "Connexion utilisable, mais latence ou débit en retrait."
        case "Mauvaise": return "Connexion dégradée — la ligne ralentit l'usage au quotidien."
        case "Très mauvaise": return "Connexion fortement dégradée — la ligne répond très lentement."
        default: return "Test non concluant — relancez."
        }
    }
}

func analyze(_ out: String) -> QualityReport {
    var rep = QualityReport()
    if let s = firstMatch(#"Downlink capacity:\s*([\d.]+)\s*Mbps"#, in: out), let v = Double(s) { rep.downlink = v }
    if let s = firstMatch(#"Uplink capacity:\s*([\d.]+)\s*Mbps"#, in: out), let v = Double(s) { rep.uplink = v }
    if let s = firstMatch(#"Responsiveness:\s*(\w+)"#, in: out) { rep.responsiveness = s }
    if let s = firstMatch(#"Idle Latency:\s*([\d.]+)\s*milliseconds"#, in: out), let v = Double(s) { rep.idleLatencyMs = v }

    if rep.downlink == nil && rep.uplink == nil && rep.idleLatencyMs == nil && rep.responsiveness == nil {
        return rep
    }

    var score = 0
    if let lat = rep.idleLatencyMs {
        if lat < 25 { score += 3 }
        else if lat < 60 { score += 2 }
        else if lat < 150 { score += 1 }
        else if lat < 300 { score += 0 }
        else if lat < 600 { score -= 1 }
        else { score -= 2 }
    }
    if let r = rep.responsiveness {
        if r == "High" { score += 1 }
        else if r == "Low" { score -= 1 }
    }
    if let d = rep.downlink {
        if d >= 100 { score += 1 }
        else if d < 30 { score -= 1 }
    }

    switch score {
    case 4...: rep.verdict = "Excellente"; rep.emoji = "🟢"
    case 2...3: rep.verdict = "Bonne"; rep.emoji = "🟢"
    case 0...1: rep.verdict = "Moyenne"; rep.emoji = "🟡"
    case -2 ... -1: rep.verdict = "Mauvaise"; rep.emoji = "🟠"
    default: rep.verdict = "Très mauvaise"; rep.emoji = "🔴"
    }
    return rep
}

func extractSummary(_ out: String) -> String {
    let lines = out.split(separator: "\n", omittingEmptySubsequences: false).map(String.init)
    if let idx = lines.firstIndex(where: { $0.contains("SUMMARY") }) {
        return lines[(idx + 1)...].filter { !$0.isEmpty }.joined(separator: "\n")
    }
    return out
}

final class AppDelegate: NSObject, NSApplicationDelegate {
    private var statusItem: NSStatusItem!
    private var timer: Timer!
    private var pingTimer: Timer!

    private var lastIn: UInt64 = 0
    private var lastOut: UInt64 = 0
    private var hasBaseline = false

    private var latencyItem: NSMenuItem!
    private var verdictItem: NSMenuItem!
    private var downItem: NSMenuItem!
    private var upItem: NSMenuItem!
    private var infoItem: NSMenuItem!
    private var testItem: NSMenuItem!

    private var currentIface = "—"
    private var currentIP = "—"
    private var currentDown: Double = 0
    private var currentUp: Double = 0

    // Latence continue (ping)
    private var latencyEmoji: String = "⚪️"
    private var latencyLabel: String = "Mesure…"
    private var lastPingDate: Date?

    // Dernier verdict networkQuality (débit + réactivité)
    private var lastEmoji: String = "⚪️"
    private var lastVerdict: String = "Pas encore testé"
    private var lastTestDate: Date?

    private let pingInterval: TimeInterval = 30.0

    func applicationDidFinishLaunching(_ notification: Notification) {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
        statusItem.button?.font = NSFont.monospacedDigitSystemFont(ofSize: 12, weight: .regular)
        buildMenu()
        setTitle()

        let c0 = readCounters()
        lastIn = c0.inBytes
        lastOut = c0.outBytes
        hasBaseline = true

        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.tick()
        }
        if let t = timer {
            RunLoop.main.add(t, forMode: .common)
        }

        pingTimer = Timer.scheduledTimer(withTimeInterval: pingInterval, repeats: true) { [weak self] _ in
            self?.pingNow()
        }
        if let t = pingTimer {
            RunLoop.main.add(t, forMode: .common)
        }
        pingNow() // premier ping immédiat
    }

    func buildMenu() {
        let menu = NSMenu()
        latencyItem = NSMenuItem(title: "", action: nil, keyEquivalent: "")
        menu.addItem(latencyItem)
        verdictItem = NSMenuItem(title: "", action: nil, keyEquivalent: "")
        menu.addItem(verdictItem)
        menu.addItem(.separator())

        downItem = NSMenuItem(title: "", action: nil, keyEquivalent: "")
        upItem = NSMenuItem(title: "", action: nil, keyEquivalent: "")
        infoItem = NSMenuItem(title: "", action: nil, keyEquivalent: "")
        menu.addItem(downItem)
        menu.addItem(upItem)
        menu.addItem(infoItem)
        menu.addItem(.separator())

        testItem = NSMenuItem(title: "Tester la connexion (networkQuality)…",
                              action: #selector(runNetworkQuality), keyEquivalent: "t")
        testItem.target = self
        menu.addItem(testItem)
        menu.addItem(.separator())

        let quit = NSMenuItem(title: "Quitter", action: #selector(quitApp), keyEquivalent: "q")
        quit.target = self
        menu.addItem(quit)

        statusItem.menu = menu
    }

    func tick() {
        let c = readCounters()
        currentIface = c.iface
        currentIP = c.ip
        if hasBaseline {
            if c.inBytes >= lastIn { currentDown = Double(c.inBytes - lastIn) }
            if c.outBytes >= lastOut { currentUp = Double(c.outBytes - lastOut) }
        }
        lastIn = c.inBytes
        lastOut = c.outBytes
        hasBaseline = true
        setTitle()
    }

    func setTitle() {
        let s = "\(latencyEmoji) ↓ \(fmtCompact(currentDown))  ↑ \(fmtCompact(currentUp))"
        let attrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.monospacedDigitSystemFont(ofSize: 12, weight: .regular),
            .foregroundColor: NSColor.labelColor
        ]
        statusItem.button?.attributedTitle = NSAttributedString(string: s, attributes: attrs)
        latencyItem?.title = "Latence : \(latencyEmoji) \(latencyLabel)\(pingAgo())"
        verdictItem?.title = "Dernier test : \(lastEmoji) \(lastVerdict)\(testAgo())"
        downItem?.title = "↓ Download : \(fmtFull(currentDown))"
        upItem?.title = "↑ Upload : \(fmtFull(currentUp))"
        infoItem?.title = "Interface : \(currentIface) · IP : \(currentIP)"
        statusItem.button?.toolTip = "↓/↑ débit temps réel · Latence \(latencyEmoji) \(latencyLabel) · Dernier test : \(lastEmoji) \(lastVerdict)"
    }

    func pingAgo() -> String {
        guard let d = lastPingDate else { return "" }
        let sec = Int(Date().timeIntervalSince(d))
        if sec < 60 { return " (il y a \(sec) s)" }
        let min = sec / 60
        return " (il y a \(min) min)"
    }

    func testAgo() -> String {
        guard let d = lastTestDate else { return "" }
        let sec = Int(Date().timeIntervalSince(d))
        if sec < 5 { return " (à l'instant)" }
        if sec < 60 { return " (il y a \(sec) s)" }
        let min = sec / 60
        if min < 60 { return " (il y a \(min) min)" }
        return " (il y a \(min / 60) h)"
    }

    // MARK: - Ping périodique

    func pingNow() {
        DispatchQueue.global(qos: .utility).async { [weak self] in
            let ms = AppDelegate.measureLatency()
            DispatchQueue.main.async {
                self?.applyPing(ms)
            }
        }
    }

    func applyPing(_ ms: Double?) {
        lastPingDate = Date()
        if let v = ms {
            (latencyEmoji, latencyLabel) = AppDelegate.latencyVerdict(v)
        } else {
            latencyEmoji = "🔴"
            latencyLabel = "Pas de réponse"
        }
        setTitle()
    }

    static func measureLatency() -> Double? {
        if let v = ping(host: "1.1.1.1") { return v }
        return ping(host: "8.8.8.8")
    }

    static func ping(host: String) -> Double? {
        let proc = Process()
        proc.executableURL = URL(fileURLWithPath: "/sbin/ping")
        proc.arguments = ["-c", "1", "-W", "3000", host]
        let pipe = Pipe()
        proc.standardOutput = pipe
        proc.standardError = pipe
        do {
            try proc.run()
            proc.waitUntilExit()
            let data = pipe.fileHandleForReading.readDataToEndOfFile()
            let out = String(data: data, encoding: .utf8) ?? ""
            if let s = firstMatch(#"time=([\d.]+)\s*ms"#, in: out), let v = Double(s) {
                return v
            }
            return nil
        } catch {
            return nil
        }
    }

    static func latencyVerdict(_ ms: Double) -> (String, String) {
        let v = String(format: "%.0f ms", ms)
        if ms < 30 { return ("🟢", "Excellente (\(v))") }
        if ms < 60 { return ("🟢", "Bonne (\(v))") }
        if ms < 150 { return ("🟡", "Moyenne (\(v))") }
        if ms < 300 { return ("🟠", "Élevée (\(v))") }
        if ms < 600 { return ("🔴", "Très élevée (\(v))") }
        return ("🔴", "Critique (\(v))")
    }

    // MARK: - Test complet networkQuality

    @objc func runNetworkQuality() {
        statusItem.menu?.cancelTracking()
        testItem?.title = "Test en cours…"
        let proc = Process()
        proc.executableURL = URL(fileURLWithPath: "/usr/bin/networkQuality")
        let pipe = Pipe()
        proc.standardOutput = pipe
        proc.standardError = pipe
        DispatchQueue.global(qos: .userInitiated).async { [weak self] in
            do {
                try proc.run()
                proc.waitUntilExit()
                let data = pipe.fileHandleForReading.readDataToEndOfFile()
                let out = String(data: data, encoding: .utf8) ?? "(aucune sortie)"
                let summary = extractSummary(out)
                let rep = analyze(out)
                DispatchQueue.main.async {
                    self?.testItem?.title = "Tester la connexion (networkQuality)…"
                    self?.applyVerdict(rep)
                    self?.showResult(summary: summary, rep: rep)
                }
            } catch {
                DispatchQueue.main.async {
                    self?.testItem?.title = "Tester la connexion (networkQuality)…"
                    self?.showResult(summary: "Erreur : \(error.localizedDescription)",
                                     rep: QualityReport())
                }
            }
        }
    }

    func applyVerdict(_ rep: QualityReport) {
        lastEmoji = rep.emoji
        lastVerdict = rep.verdict
        lastTestDate = Date()
        setTitle()
    }

    func showResult(summary: String, rep: QualityReport) {
        let alert = NSAlert()
        alert.messageText = "État de la connexion : \(rep.emoji) \(rep.verdict)"
        var info = summary
        let expl = rep.explanation()
        if !expl.isEmpty { info += "\n\n\(expl)" }
        alert.informativeText = info
        alert.alertStyle = .informational
        alert.addButton(withTitle: "OK")
        alert.runModal()
    }

    @objc func quitApp() {
        NSApp.terminate(nil)
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.setActivationPolicy(.accessory)
app.run()
