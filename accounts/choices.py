
DESIGNATION = (
    (1,'ASSISTANT PROFESSOR'),
    (2,'ASSOCIATE PROFESSOR'),
    (3,'PROFESSOR'),
)

USER_TYPES = (
    (1,'FACULTY'),
    (2,'ACCOUNT'),
    (3,'REGISTRAR'),
    (4,'DIRECTOR'),
    (5,'PURCHASE')
)

DEPARTMENT = (
    ('NA', 'NOT APPLICABLE'),
    ('CSE', 'COMPUTER SCIENCE AND ENGINEERING'),
    ('ECE', 'ELECTRONICS AND COMMUNICATION ENGINEERING'),
    ('ME', 'MECHANICAL ENGINEERING'),
    ('EE', 'ELECTRICAL ENGINEERING'),
    ('EI', 'ELECTRONICS & INSTRUMENTATION ENGINEERING'),
    ('CE', 'CIVIL ENGINEERING'),
)

EMPLOYEE_TYPE = (
    ('FT', 'FULL TIME'),
    ('PT', 'PART TIME'),
    ('C', 'CONTRACTUAL'),
    ('V', 'VISITING'),
)

BOOLEAN = (
    ('N', 'NO'),
    ('Y', 'YES'),
)

PURCHASE_STATUS = (
    # (0, 'Purchase Request Saved in Draft'),
    # (1, 'Purchase Request is with HOD'),
    (0, 'Waiting for approval by HOD'),
    # (3, 'Purchase Request is in Account Section'),
    (1, 'Waiting for Approval by Account Section'),
    (2, 'Waiting for Approval by Registrar'),
    (3, 'Waiting for Approval by Director'),
    # (7, 'Approved by Account Section'),
    (4, 'Purchase Request at Purchase Section'),
    (5, 'Product Purchased'),
    (6, 'Purchase denied'),
)

ACADEMIC_SESSION = [
    (2018,'2018-19'),
    (2019,'2019-20'),
    (2020,'2020-21'),
    (2021,'2021-22'),
    (2022,'2022-23'),
    (2023,'2023-24'),
]
