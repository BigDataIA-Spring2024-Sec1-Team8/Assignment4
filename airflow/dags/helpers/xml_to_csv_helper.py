import xml.etree.ElementTree as ET
import csv
import os
from lxml import etree

def convert_xml_to_csv(run_id, xml_file_name='Level1_combined.grobid.tei.xml'):
    dags = os.path.join(os.getcwd(), 'dags')
    res_path = os.path.join(dags, 'resources')
    res_path = os.path.join(res_path, str(run_id))
    csv_filename=xml_file_name.replace('grobid.tei.xml', 'csv')
    c1 = os.path.join(res_path,csv_filename)
    xml1 = os.path.join(res_path, xml_file_name)
    xml_file_paths = [xml1]
    print(xml_file_paths)
    with open(c1, 'w+', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write header
        csv_writer.writerow(['Topic', 'Learning_Outcomes_Section'])
        
        # Iterate through each XML file
        for xml_file_path in xml_file_paths:
            print(xml_file_path)
            # Read the XML data from the file
            with open(xml_file_path, 'r') as file:
                xml_data = file.read()
            # Parse the XML data
            root = ET.fromstring(xml_data)

            for div_element in root.findall('.//{http://www.tei-c.org/ns/1.0}div'):
                    head_element = div_element.find('.//{http://www.tei-c.org/ns/1.0}head')

                    p_elements = div_element.findall('.//{http://www.tei-c.org/ns/1.0}p')

                    combined_p_text = ' '.join(p_element.text for p_element in p_elements if p_element.text)
                    if combined_p_text != '':
                        csv_writer.writerow([head_element.text if head_element is not None else 'Not Available', combined_p_text])
                    else:
                        csv_writer.writerow([head_element.text if head_element is not None else 'Not Available', 'Not Available'])

    return csv_filename


def convert_xml_to_metadata(run_id, xml_file_name='Level1_combined.grobid.tei.xml'):
    """
    Extracts metadata from an XML file using XPath expressions and appends the information to a list.

    Parameters:
    - path (str): The path to the XML file.
    - pdf_content_list (list): A list to which extracted metadata dictionaries will be appended.
    - bucket_links (dict): A dictionary containing links to S3 buckets corresponding to XML files.

    Returns:
    None
    """
    # Get the absolute path of the XML file
    dags = os.path.join(os.getcwd(), 'dags')
    res_path = os.path.join(dags, 'resources')
    res_path = os.path.join(res_path, str(run_id))
    print(res_path)
    csv_filename=xml_file_name.replace('.grobid.tei.xml', '_metadata.csv')
    # Parse the XML file
    print(csv_filename)
    c1 = os.path.join(res_path,csv_filename)
    xml_file_path = os.path.join(res_path, xml_file_name)
    file_name = csv_filename.replace('.csv', '')
    with open(c1, 'w+', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write header
        csv_writer.writerow(['PDF_NAME','Title', 'Publisher', 'AvailabilityStatus', 'Analytic', 'ImprintedDate','AppInfoDescription','Abstract' ])
        
        if os.path.exists(xml_file_path):
            tree = etree.parse(xml_file_path)
            root = tree.getroot()
        # Define XML namespaces
            namespaces = {
                'tei': 'http://www.tei-c.org/ns/1.0',
                'xlink': 'http://www.w3.org/1999/xlink'
            }

            def get_first_item(xpath_result):   
                if xpath_result:
                    # Remove newline and tab characters and return the first item
                    xpath_result[0] = xpath_result[0].replace('\n', '').replace('\t','')
                    return f"{xpath_result[0]}"  
                else:
                    return "No Data"

            # Extract metadata using XPath expressions
            metadata_dict = {
                "Title": get_first_item(root.xpath('//tei:titleStmt/tei:title[@level="a" and @type="main"]/text()', namespaces=namespaces)),
                "Publisher": get_first_item(root.xpath('//tei:publicationStmt/tei:publisher/text()', namespaces=namespaces)),
                "AvailabilityStatus": get_first_item(root.xpath('//tei:availability/@status', namespaces=namespaces)),
                "Analytic": get_first_item(root.xpath('//tei:analytic/text()', namespaces=namespaces)),
                "ImprintedDate": get_first_item(root.xpath('//tei:imprint/tei:date/text()', namespaces=namespaces)),
                "AppInfoDescription": get_first_item(root.xpath('//tei:application/tei:desc/text()', namespaces=namespaces)),
                "Abstract": get_first_item(root.xpath('//tei:profileDesc/tei:abstract/tei:p/text()', namespaces=namespaces)),
            }
            print(file_name, metadata_dict)
            csv_writer.writerow([file_name,metadata_dict['Title'], metadata_dict['Publisher'],metadata_dict['AvailabilityStatus'],metadata_dict['Analytic'],metadata_dict['ImprintedDate'],metadata_dict['AppInfoDescription'],metadata_dict['Abstract']])
    return csv_filename