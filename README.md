# bizdoc
Business Document Processing


mysql> select * from company
    -> ;
+----+------------------------------------+---------------------------------------------------------------------------------------------------------+
| ID | company_name                       | po_customization                                                                                        |
+----+------------------------------------+---------------------------------------------------------------------------------------------------------+
|  1 | MCDONALD PRIMARY                   | NULL                                                                                                    |
|  2 | KEHE FOOD DISTRIBUTORS INC         | NULL                                                                                                    |
|  3 | BEN E. KEITH CO.                   | NULL                                                                                                    |
|  4 | MCDONALD SECONDARY                 | NULL                                                                                                    |
|  5 | BIRITE FOODSERVICE DISTRIBUTORS    | NULL                                                                                                    |
|  6 | 5 ETHAN SURRETT                    | EXTRACT RUN DATE as po_date, ignore DUE DATE                                                            |
|  7 | IMPERIAL DADE CITY OF INDUSTRY     | NULL                                                                                                    |
|  8 | TJX COMPANIES                      | NULL                                                                                                    |
|  9 | SOUTHERN GLAZER'S WINE AND SPIRITS | NULL                                                                                                    |
| 10 | EPICUREAN FINE FOODS INC           | NULL                                                                                                    |
| 11 | SYSCO                              | Ignore the date after "TO BE DELIVERED:....", PO date is at the complete end of the text after "Thanks" |
| 12 | PERFORMANCE FOODSERVICE - MIDLANDS | PO date is called "RUN DATE", ignore "DUE DATE"                                                         |
| 13 | PERFORMANCE FOODSERVICE - JACKSON  | PO date is called "RUN DATE", ignore "DUE DATE"                                                         |
| 14 | PERFORMANCE FOODSERVICE - ALABAMA  | PO date is called "RUN DATE", ignore "DUE DATE"                                                         |
| 15 | Wendling's Food Service            | NULL                                                                                                    |
+----+------------------------------------+---------------------------------------------------------------------------------------------------------+
15 rows in set (0.00 sec)
