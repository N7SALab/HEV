def credential_db():
    """Hard coded credentials encrypted with bcrypt
    
    :return: credential database
    """

    # TODO: Encrypt user names
    # TODO: use an actual database

    credentials = {
        # 'admin': b'disabled',
        # 'test': b'disabled',
        'hev@hev': b'$2b$12$c.A//7LqYwWyEJXFOZ.ymuoJUwKfMJgl5zXGEbtaJ2gSCZBWtj/Hy',
        'hev@hev': b'$2b$12$R/0oHYkBwx.Sf9HX2yC4WubRnfFbH/JuovztgQuhYGiKDgz2gdYHy',
    }

    return credentials
