USER_TYPES = (
    (1,'FACULTY'),
    (2,'ACCOUNT'),
    (3,"DIRECTOR"),
    (4,'PURCHASE'),
)

DESIGNATION = (
    (1,'ASSISTANT PROFESSOR'),
    (2,'ASSOCIATE PROFESSOR'),
    (3,'PROFESSOR'),
)

DEPARTMENT = (
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
    (0, 'Purchase Request Generated'),
    (1, 'Waiting for approval by HOD'),
    (2, 'Approved by HOD'),
    (3, 'Waiting for Approval by Account Section'),
    (4, 'Approved by Account Section'),
    (5, 'Purchase Request at Purchase Section'),
    (6, 'Product Purchased'),
    (7, 'Purchase denied'),
)
