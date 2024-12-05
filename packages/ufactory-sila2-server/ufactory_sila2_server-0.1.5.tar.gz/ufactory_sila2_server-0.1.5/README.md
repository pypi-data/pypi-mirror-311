# 📂 SiLA API for Lite6 Robotic Arm

This project provides a **SiLA 2 Wrapper** for controlling a **uFactory Lite 6 robotic arm** using the SiLA 2 standard. It enables seamless and standardized control of the Lite 6 robotic arm for various applications.

## 📑 Table of Contents

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Start the SiLA Server](#step-2-start-the-sila-server)
  - [Step 3: Start the SiLA Browser](#step-3-start-the-sila-browser)
- [Contact](#contact)

## 🛠 Installation

Follow these steps to set up and run the project on your local machine.

### Prerequisites

Ensure you have the following software and dependencies installed:

- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/) (version 14 or above recommended)
- [Python](https://www.python.org/) (version 3.6 or above recommended)
- [xArm-Python-SDK](https://github.com/xArm-Developer/xArm-Python-SDK) for controlling the Lite 6 robotic arm
- [Sila Browser](https://gitlab.com/unitelabs/sila2/sila-browser) for interacting with SiLA services in a browser interface

### Step 1: Clone the Repository

1. **Clone this repository** to your local machine:

    ```bash
    git clone https://git.fhict.nl/coe-htsm/sila-api-for-lite6.git
    ```

2. **Verify xArm API reference**:
    - In `UF_Controller/feature_implementations/ufcontroller_impl.py`, ensure the `XArmAPI` import is correctly referenced:

    ```python
    from xarm.wrapper import XArmAPI
    ```

    - If this reference does not automatically detect the SDK, manually add the path to the `xArm-Python-SDK` folder in your project structure.

3. **Set the robotic arm IP address**:
    - In the same file, ensure that the `arm_ip` variable is set to the correct IP address of your robotic arm.
    - **Note**: If you're unsure of the arm’s IP, you can find it on the back of the robot or in the device manual.

### Step 2: Start the SiLA Server

To start the SiLA server, open a terminal and run the following command:

```bash
python -m UF_Controller --insecure
```
This command launches the SiLA interface for controlling the Lite 6 robotic arm.

### Step 3: Start the SiLA Browser
1. **Install and configure the SiLA Browser**  by following setup instructions provided in the [SiLA Browser repository](https://gitlab.com/unitelabs/sila2/sila-browser).

2. Once installed, start the local server using:
```bash
npm run preview
```
3. **Accss the SiLA Browser:
- Open your browser and go to the following URL to access the SiLA services:
```text
http://localhost:3000/127.0.0.1:50052
```
This should connect you to the SiLA Browser interface for managing your robotic arm.

## 📬 Contact
Leave me a message at *b.marinov@fontys.nl* can you make it better