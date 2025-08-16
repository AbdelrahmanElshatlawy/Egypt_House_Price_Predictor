# House Price Prediction in Egypt

**House Price Prediction in Egypt** is a data-driven project that combines **web scraping**, **data analysis**, and **machine learning** to estimate real estate prices across different regions of Egypt. The project demonstrates the end-to-end workflow from data collection to predictive modeling.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Data Acquisition](#data-acquisition)
* [Data Preprocessing](#data-preprocessing)
* [Exploratory Data Analysis](#exploratory-data-analysis)
* [Feature Engineering](#feature-engineering)
* [Model Development](#model-development)
* [Model Evaluation](#model-evaluation)
* [Usage](#usage)
* [Dependencies](#dependencies)
* [License](#license)

---

## Project Overview

The primary objective of this project is to **predict property prices** in Egypt using features such as:

* Area in square meters
* Number of bedrooms and bathrooms
* Unit type (apartment, villa, etc.)
* Geographic information (region and locality)

The workflow includes:

1. Scraping property listings from [Bayut Egypt](https://www.bayut.eg/en/egypt/properties-for-sale/).
2. Cleaning and preprocessing the collected data.
3. Conducting exploratory data analysis (EDA) to understand key trends.
4. Feature engineering to enhance model performance.
5. Training an XGBoost regression model to predict house prices.

---

## Data Acquisition

The dataset is collected through **web scraping** using Python libraries:

* `requests` for HTTP requests
* `BeautifulSoup` for HTML parsing

Key steps:

1. Extract structured JSON-LD data from each property listing.
2. Capture attributes such as:

   * Name
   * Latitude & Longitude
   * Area (Sq. M.)
   * Bedrooms & Bathrooms
   * Region & Locality
   * Unit type
   * Price (EGP)

The scraped data is saved as `units_details.csv`.

---

## Data Preprocessing

* Removal of missing or incomplete records.
* Type conversions for numeric fields (e.g., `bedrooms`, `bathrooms`, `price`).
* Rounding and normalization where necessary.
* Handling categorical variables via **one-hot encoding** for region, locality, and unit type.
* Creation of derived features:

  * `room_bath_ratio` = bedrooms / (bathrooms + ε)
  * `price_per_sqm` = price / area

---

## Exploratory Data Analysis (EDA)

Visualizations are used to explore the dataset and detect patterns:

* Distribution of house prices using histograms and scatter plots.
* Impact of bathrooms on pricing through count plots, boxplots, and strip plots.
* Identification of potential outliers and trends in property features.

These insights inform feature selection and preprocessing decisions.

---

## Feature Engineering

The project leverages engineered features to improve predictive performance:

* Categorical features (`region`, `unit_type`, `locality`) are transformed via **one-hot encoding**.
* Numerical features include:

  * `room_bath_ratio`
  * `price_per_sqm`
* Unnecessary columns (e.g., `name`, original categorical columns) are dropped.

Target variable `price(EGP)` is transformed using `log1p` to stabilize variance and mitigate skewness.

---

## Model Development

* **Train/Test split**: 80% training, 20% testing
* **Model**: XGBoost Regressor

  * `n_estimators=500`
  * `learning_rate=0.05`
  * `max_depth=6`
  * `subsample=0.8`
  * `colsample_bytree=0.8`
  * Objective: `reg:squarederror`

The model is trained on the processed feature set and evaluated on the held-out test set.

---

## Model Evaluation

Predictions are evaluated using:

* **Mean Squared Error (MSE)**
* **Root Mean Squared Error (RMSE)**
* **R² Score**

Additionally, 10 random test samples are selected to compare **predicted vs. actual prices** (after reversing the log transformation).

**Actual Model Predictions Example**:

| Actual Price (EGP) | Predicted Price (EGP) |
| ------------------ | --------------------- |
| 11,000,000.0       | 10,859,325            |
| 8,000,000          | 7,922,924             |
| ...                | ...                   |

This provides a tangible demonstration of model performance.

---

## Usage

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/house-price-prediction.git
cd house-price-prediction
```

