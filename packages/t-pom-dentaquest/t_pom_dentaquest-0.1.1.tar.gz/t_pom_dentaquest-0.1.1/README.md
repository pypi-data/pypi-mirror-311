# T_pom_dentaquest 📦

> **A Python package for DentaQuest POM approach
            when interacting with web pages and their elements.**

## 📑 Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage Example](#usage-example)
- [API Documentation](#api-documentation)
- [License](#license)

## Overview
This package provides DentaQuest portal Base class, web pages and web elements.
            
There are also usable web elements that have commonly used methods built in.

## Installation
```bash
pip install t-pom-dentaquest
```

## Usage Example
For detailed examples, please refer to our
            [quick start page](https://www.notion.so/thoughtfulautomation/T-DentaQuest-14bf43a78fa480d0a974e4d6be1f763c).

### 
## API Documentation

---

## Decorators
### Module: `t_pom_dentaquest.decorators`

_Module for the decorator._

- **Function:** `relogin_and_retry_if_error`
  > Decorator to relogin and retry the function if a Web-related error occurs.

---

## Elements
### Module: `t_pom_dentaquest.elements`

_Module for all web app elements._

### Module: `t_pom_dentaquest.elements.container_element`

_Select container element module._

- **Class:** `ContainerElement`
  > Class for container elements.
  - **Method:** `check_if_all_elements_contain_value`
    > Get text for each attribute in object with matching id.
### Module: `t_pom_dentaquest.elements.select_dropdown_element`

_Select dropdown element module._

- **Class:** `SelectDropdownElement`
  > Class for select dropdown elements.
  - **Method:** `select_options`
    > Select options from the dropdown list.
### Module: `t_pom_dentaquest.elements.table_element`

_Table element module._

- **Class:** `TableElement`
  > Class for table elements.
  - **Method:** `get_summary_table_data`
    > Extracts and structures data from an HTML summary table into a list of dictionaries.

        This method locates the table headers and body rows, then iterates over them to extract the data.
        Each row of the table is represented as a dictionary.

        Returns:
            list: A list of dictionaries, where each dictionary represents a row in the table.
                Each dictionary key is a column header, and each value is the corresponding data
                from that column in the row.
        
  - **Method:** `get_table_data`
    > Extracts data from an HTML table.

        This method locates table headers and body elements, then iterates over them to extract and structure the data
        into a dictionary.

        Returns:
            dict: A dictionary where each key is a table name and each value is another dictionary containing
            the column names and their respective values.
        
### Module: `t_pom_dentaquest.elements.text_element`

_Text element module._

- **Class:** `TextElement`
  > Class for input element model.

---

## Pages
### Module: `t_pom_dentaquest.pages`

_Page modules for DentaQuest._

### Module: `t_pom_dentaquest.pages.home_page`

_Generic home page for web app._

- **Class:** `HomePage`
  > Page class containing elements specific to a home page interface.
### Module: `t_pom_dentaquest.pages.login_page`

_Generic login page for web app._

- **Class:** `LoginPage`
  > Page class containing elements specific to a login interface.
### Module: `t_pom_dentaquest.pages.member_detail_page`

_Generic member detail page for web app._

- **Class:** `MemberDetailPage`
  > Page class containing elements specific to a login interface.
### Module: `t_pom_dentaquest.pages.member_eligibility_list_page`

_Generic login page member eligibility list web app._

- **Class:** `MemberEligibilityListPage`
  > Page class containing elements specific to a member eligibility list page interface.
### Module: `t_pom_dentaquest.pages.member_eligibility_search_page`

_Generic member eligibility search page for web app._

- **Class:** `MemberEligibilitySearchPage`
  > Page class containing elements specific to a member eligibility search page interface.
### Module: `t_pom_dentaquest.pages.plan_benefit_summary_page`

_Generic plan benefits summary page for web app._

- **Class:** `PlanBenefitSummaryPage`
  > Page class containing elements specific to a plan benefits summary page interface.

---

## T_dentaquest
### Module: `t_pom_dentaquest.t_dentaquest`

_Generic base class for web app._

- **Class:** `TDentaQuest`
  > Main application class managing pages and providing direct access to Selenium.

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
