CREATE DATABASE bizdoc_db;

create table bixdoc_db.company (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
	po_customization VARCHAR(1000)
    );


CREATE TABLE bizdoc_db.order_details (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    po_number VARCHAR(50),
    po_date DATE,
    product_num VARCHAR(50),
    prod_description TEXT,
    quantity INT,
    unit_cost DECIMAL(10, 2),
    amount DECIMAL(10, 2)
);

INSERT INTO bizdoc_db.company (company_name) VALUES
('FEESERS INC.'),
('INTERNATIONAL CRUISE F&H SUPPLIERS'),
('MCDONALD PRIMARY'),
('KEHE FOOD DISTRIBUTORS INC'),
('BEN E. KEITH CO.'),
('MCDONALD SECONDARY'),
('BIRITE FOODSERVICE DISTRIBUTORS'),
('5 ETHAN SURRETT'),
('IMPERIAL DADE CITY OF INDUSTRY'),
('TJX COMPANIES'),
('SOUTHERN GLAZER''S WINE AND SPIRITS'),
('EPICUREAN FINE FOODS INC'),
('SYSCO'),
('PERFORMANCE FOODSERVICE - MIDLANDS'),
('PERFORMANCE FOODSERVICE - JACKSON'),
('PERFORMANCE FOODSERVICE - ALABAMA'),
('Wendling''s Food Service');

UPDATE bizdoc_db.company
SET po_customization = 'Here, extract RUN DATE as po_date, ignore DUE DATE. '
WHERE company_name = '5 ETHAN SURRETT';

UPDATE bizdoc_db.company
SET po_customization = 'Ignore the date after "TO BE DELIVERED:....", PO date is at the complete end of the text after "Thanks"'
WHERE company_name = 'SYSCO';

UPDATE bizdoc_db.company
SET po_customization = 'PO date is called "RUN DATE" ignore "DUE DATE". Product Number is called "Manuf#" - it is NOT alphanumeric. Quantity is called "Qty"'
WHERE company_name like 'PERFORMANCE FOODSERVICE%';

UPDATE bizdoc_db.company
SET po_customization = 'PO Number is mentioned after "** NUMBER -". Product Number is called "Item #". Quantity is called "Order", mentioned right before "|____|"'
WHERE company_name = 'FEESERS INC.';

UPDATE bizdoc_db.company
SET po_customization = 'PO Date is the FIRST Date. Quantity is mentioned after description. It is given as a WHOLE NUMBER, NOT DECIMAL'
WHERE company_name = 'BEN E. KEITH CO.';

UPDATE bizdoc_db.company
SET po_customization = 'Product Number is called "Item #" and Quantity is called "Order"'
WHERE company_name = 'BIRITE FOODSERVICE DISTRIBUTORS';

UPDATE bizdoc_db.company
SET po_customization = 'Quantity is called "Ordered" - given in the FIRST column. Product Number is called "Item Code" - second column. Make sure to not miss the first entry'
WHERE company_name = 'INTERNATIONAL CRUISE F&H SUPPLIERS';

select * from bizdoc_db.company where po_customization is not null;

SELECT company_name
FROM bizdoc_db.company
GROUP BY company_name
HAVING COUNT(company_name) > 1;
