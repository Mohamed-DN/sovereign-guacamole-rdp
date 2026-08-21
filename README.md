# 🥑 Sovereign Guacamole RDP

Welcome to the **Sovereign Guacamole RDP** project! 
This is the ultimate, zero-touch "Black Magic" solution for deploying a professional Remote Desktop system (Apache Guacamole) completely automatically.

Normally, installing Guacamole requires dozens of manual steps, complex database initializations, and endless clicks to add connections. 
This repository **does everything for you**: it installs the servers, creates your custom secure user, destroys the default insecure accounts, adds your Windows computer connection, and injects graphics optimizations to eliminate lag. **All in 1-Click.**

---

## 🏗️ Architecture Flow

```mermaid
graph TD
    classDef user fill:#2563eb,stroke:#1d4ed8,stroke-width:2px,color:#fff,rx:8px,ry:8px;
    classDef proxy fill:#f59e0b,stroke:#b45309,stroke-width:2px,color:#fff,rx:8px,ry:8px;
    classDef guacWeb fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff,rx:8px,ry:8px;
    classDef guacDaemon fill:#8b5cf6,stroke:#6d28d9,stroke-width:2px,color:#fff,rx:8px,ry:8px;
    classDef database fill:#64748b,stroke:#334155,stroke-width:2px,color:#fff,rx:100px,ry:100px;
    classDef vm fill:#ef4444,stroke:#b91c1c,stroke-width:2px,color:#fff,rx:8px,ry:8px;

    Client["🖥️ User Browser"]:::user
    NPM["🛡️ Nginx Proxy Manager<br/>(HTTPS / SSL)"]:::proxy
    
    subgraph "Docker Bridge Network"
        Web["🌐 Guacamole Web<br/>(Tomcat :8080)"]:::guacWeb
        Guacd["⚙️ Guacd Daemon<br/>(Native C Proxy)"]:::guacDaemon
        DB[("🗄️ PostgreSQL 15<br/>(Users & Config)")]:::database
    end

    WinVM["🪟 Windows Work VM<br/>(RDP)"]:::vm
    Drive["📁 Shared RDP Drive<br/>(Docker Volume)"]:::database

    Client -- "HTTPS (443)" --> NPM
    NPM -- "HTTP (8080)" --> Web
    Web -- "Auth & Config" --> DB
    Web -- "Guacamole Protocol" --> Guacd
    Guacd -- "RDP (3389)" --> WinVM
    Guacd -. "File Transfer" .- Drive
    WinVM -. "Mapped Network Drive" .- Drive
```

---

## 🚀 How to Install (1-Click Deployment)

If you are not a technical expert, don't worry! Just follow these three simple steps:

1. **Clone this repository** onto your target server (e.g., inside a Proxmox LXC container).
2. **Enter the directory**:
   ```bash
   cd sovereign-guacamole-rdp
   ```
3. ⚠️ **CRITICAL CONFIGURATION:** Open the `START_HERE.sh` file with a text editor (like `nano START_HERE.sh`) and edit the configuration variables at the top. You **MUST** enter your target Windows machine's IP address, or the automation will fail to connect. You can also customize your new admin username and password here.
   ```bash
   export GUAC_USER="admin"
   export GUAC_PASS="SuperSecurePassword123!"
   export WINDOWS_IP="192.168.1.100" # <-- CHANGE THIS
   ```
4. **Start the automated installation** (The Black Magic 🧙‍♂️) by running:
   ```bash
   bash START_HERE.sh
   ```

**Done!** The script will run on its own for a few seconds, download all necessary components, and automatically configure every single detail for you using the IPs and credentials you provided.

---

## 🌐 Exposing to the Internet (Nginx Proxy Manager)

*This is the most critical part!* The Guacamole system is now running on your server, but to access it securely from outside your home (e.g., `https://guacamole.yourdomain.com`) with the Green Padlock (SSL), **you must use Nginx Proxy Manager (NPM)**.

Here is the **STEP-BY-STEP** guide (word for word) on exactly what to click inside Nginx Proxy Manager:

### 1. Add the Proxy Host
1. Open your **Nginx Proxy Manager** dashboard.
2. Click on **Hosts** in the top menu, then select **Proxy Hosts**.
3. Click the green **Add Proxy Host** button in the top right corner.

### 2. Configure the "Details" Tab
In the window that opens, fill out the fields *exactly* like this:
- **Domain Names:** Type your personal domain (e.g., `guacamole.yourdomain.com`) and press Enter.
- **Scheme:** Leave it as `http`
- **Forward Hostname / IP:** Type the local IP address of the server where you just installed Guacamole (e.g., `192.168.1.X_SERVER_IP`, or `127.0.0.1` if NPM is on the exact same machine).
- **Forward Port:** Type `8080`
- **Cache Assets:** Check the box (Enabled)
- **Block Common Exploits:** Check the box (Enabled)
- **Websockets Support:** Check the box (Enabled) ⚠️ *CRITICAL! Without this, your mouse and keyboard will not work in Guacamole!*

### 3. Configure the "SSL" Tab (The Green Padlock)
Now click on the "SSL" tab at the top of the same window:
- **SSL Certificate:** Click the dropdown menu and select **Request a new SSL Certificate**.
- **Force SSL:** Check the box (Enabled). This forces everyone to use the secure HTTPS connection.
- **Email Address for Let's Encrypt:** Enter your real email address. This is required to generate the security certificate automatically.
- **I Agree to the Let's Encrypt Terms of Service:** Check the box (Enabled).
- Finally, click **Save**.

Wait a few seconds. If everything is correct, the window will close and your domain will be online!
Now go to your browser, type `https://guacamole.yourdomain.com/guacamole/` and you are securely inside your remote computer!

---

## ✨ What does the "Black Magic" do in the background?

When you run `START_HERE.sh`, we automate the ultimate "Best Practices" without you moving a finger:

- **Zero-Touch Deployment:** PostgreSQL, Guacd, and Tomcat boot up inside an isolated, secure Docker network.
- **Auto-Security:** The default `guacadmin` user is permanently destroyed to prevent brute-force attacks.
- **Extreme RDP Performance:** To eliminate stutter and input lag, we inject these parameters directly into the Guacamole engine:
  - `16-bit color depth` (Saves 50% of bandwidth)
  - `Disable Wallpaper` (Instant desktop loading)
  - `Disable Animations & Themes` (Zero input lag)
- **Shared Drive (File Transfer):** Automatically creates a virtual "Network Drive" between your browser and the Windows machine. You can drag-and-drop files directly into your browser window, and they will instantly appear inside the virtual drive on Windows!

---

## 📜 Architecture Deep Dive & Legacy Scripts

- **Want to know how it works under the hood?** Read the [Full Architecture Guide (S.O.A.P.)](docs/FULL_GUIDE.md).
- **Looking for the original Python codes?** All the raw original Python scripts we wrote to reverse-engineer this technology in our Homelab have been sanitized and preserved in the `scripts/legacy_homelab` folder. Everything else has been merged into the master `scripts/deploy.sh`.
