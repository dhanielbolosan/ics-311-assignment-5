 'Rapanui': {'Tonga'},
        'New Zealand': {'Samoa', 'Tonga', 'Hawaii'},
        'Samoa': {'Hawaii', 'Tonga'},
        'Tonga': {'Hawaii', 'Samoa', 'New Zealand', 'Rapanui'}
    }

    # Example edges with weights
    exps = [
        ('Hawaii', 'Samoa', 1),
        ('Hawaii', 'Tonga', 2),
        ('Hawaii', 'New Zealand', 3),
        ('Rapanui', 'Tonga', 4),
        ('New Zealand', 'Samoa', 2),
        ('New Zealand', 'Tonga', 2),
        ('Samoa', 'Tonga', 1),
        ('Tonga', 'Rapanui', 4),
    ]