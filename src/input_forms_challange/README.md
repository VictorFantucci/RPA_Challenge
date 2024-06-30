# RPA Challenge Automation - Input Forms

## About the Project

This project was developed based on the 'RPA Challenge' exercise proposed on the [RPA Challenge](https://rpachallenge.com/) website.

The **RPA Challenge** is a web application designed for RPA (Robotic Process Automation) training. The challenge involves downloading an XLSX file, reading its data, and filling out a form on the website. The primary difficulty is that the form fields are dynamic and change positions with each data entry, requiring precise mapping of the input element selectors.

In this project, the selectors of the elements were mapped using Xpath.

At the end of the data entry, the page displays a message showing the time the robot took to execute the task. The robot then translates this message and captures a screenshot of the screen, saving it in the project folder.

## Features

- Download the XLSX file from the website.
- Read data from the XLSX file.
- Dynamically map form fields using Xpath.
- Fill out the form with data from the XLSX file.
- Translate the execution time message displayed at the end.
- Capture and save a screenshot of the final screen.

## Prerequisites

- Python 3.x
- Python libraries: `pandas`, `openpyxl`, `selenium`, `pillow`, `googletrans`
- Webdriver compatible with the browser in use (e.g., `chromedriver` for Google Chrome)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/rpa-challenge-automation.git
   cd rpa-challenge-automation
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Download the Webdriver compatible with your browser and add it to the system PATH.

## Usage

1. Run the main script:

   ```bash
   python -m src.input_forms_challenge.input_forms_challenge
   ```

2. The robot will download the XLSX file, read the data, fill out the form on the website, and display the execution time message, which will be translated and captured as a screenshot.

## Project Structure

```
rpa-challenge-automation/
│
├── data/
│   └── challenge.xlsx         # Downloaded XLSX file
│
├── screenshots/
│   └── result.png             # Final screen screenshot
│
├── src/
│   └── input_forms_challenge/
│      └── input_forms_challenge.py
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Contributing

1. Fork the project.
2. Create a branch for your feature (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

Feel free to contribute improvements and new features to this project!
