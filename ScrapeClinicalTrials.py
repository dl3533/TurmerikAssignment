from playwright.sync_api import sync_playwright
import csv
import time

def scrape_clinical_trials():

    # Remove or edit this line when running on your own machine as this path is specific to my machine
    file_path = r'C:\Users\david\TurmerikAssignment\clinical_trials.csv'


    # Open a CSV file to save the trial names
    with open('clinical_trials.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Trial:', 'Age:', 'Gender:', 'Inclusion Criteria:', 'Exclusion Criteria:']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Run in headless mode
            page = browser.new_page()
            
            page.goto("https://clinicaltrials.gov/search?aggFilters=status:rec")
            
            # Wait for the trial listings to load
            page.wait_for_selector('ctg-search-hit-card header > a')
            current_page = 1

            #scrape titles for i pages
            for i in range(1):

                # Extract title content
                titles = page.query_selector_all('ctg-search-hit-card header > a')
                
                # Write each title to the CSV
                for title in titles:
                    title_name = title.inner_text().strip()

                    #go to the actual page to get inclusion/exclusion data
                    title = page.query_selector('ctg-search-hit-card header > a')
                    title.click(force=True)
                    
                    # Wait for the trial page to load
                    page.wait_for_selector('#main-content > ctg-study-details > section > ctg-study-details-top-info > div.desktop\:margin-bottom-4.margin-bottom-2 > h2') 
                    
                    #scrape the necessary data and convert it into text for our purposes
                    age = page.query_selector('#participation-criteria > ctg-participation-criteria > div.usa-prose.margin-top-4.participation-content > div > div.grid-row.grid-gap.row-overview > div.right-col > div:nth-child(2) > ctg-standard-age > span:nth-child(1)')
                    gender = page.query_selector('#participation-criteria > ctg-participation-criteria > div.usa-prose.margin-top-4.participation-content > div > div.grid-row.grid-gap.row-overview > div.right-col > div:nth-child(4) > ctg-enum-value > span')
                    inclusion = page.query_selector('#eligibility-criteria-description > div > div > ul:nth-child(2)')
                    exclusion = page.query_selector('#eligibility-criteria-description > div > div > ul:nth-child(4)')

                    age_text = age.inner_text().strip() if age else 'N/A'
                    gender_text = gender.inner_text().strip() if gender else 'N/A'
                    inclusion_text = inclusion.inner_text().strip() if inclusion else 'N/A'
                    exclusion_text = exclusion.inner_text().strip() if exclusion else 'N/A'

                    # Write the row with trial data
                    writer.writerow({
                        'Trial:': title_name, 
                        'Age:': age_text, 
                        'Gender:': gender_text, 
                        'Inclusion Criteria:': inclusion_text, 
                        'Exclusion Criteria:': exclusion_text
                    })

                    # Go back to the search results page
                    page.go_back()

                    # Wait for the search results page to load
                    page.wait_for_selector('ctg-search-hit-card header > a')



                next_button_selector = '#paginatorContainer > pagination-template > ctg-pagination-uswds > div > nav > ul > li:nth-child(10) > button'
                next_button = page.query_selector(next_button_selector)
                next_button.click()
                current_page += 1
                page.wait_for_selector('ctg-search-hit-card header > a', timeout = 5000)
            
            # Close the browser
            browser.close()

if __name__ == "__main__":
    scrape_clinical_trials()

