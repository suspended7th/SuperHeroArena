import pytest, re

@pytest.fixture()
def app(app_setup):
    yield app_setup

def test_new_user_endpoints(app, client):
    # Test that the endpoint functions properly
    response = client.get('/supers/')
    assert response.status_code == 200
    assert len(re.findall(r'<img\s', str(response.data))) == 0
    
    # Test that a 10 random heroes can be retrieved
    response = client.get(
        '/supers/',
        query_string = {
            'heroes': 'true'
        }
    )
    assert response.status_code == 200
    data = str(response.data)
    assert len(re.findall(r'<img\s', data)) == 20
    assert len(re.findall(r'<td>bad</td>', data)) == 0
    assert len(re.findall(r'<td>good</td>', data)) == 20
    
    # Test that a 10 random villains can be retrieved
    response = client.get(
        '/supers/',
        query_string = {
            'villains': 'true'
        }
    )
    assert response.status_code == 200
    data = str(response.data)
    assert len(re.findall(r'<img\s', data)) == 20
    assert len(re.findall(r'<td>bad</td>', data)) == 20
    assert len(re.findall(r'<td>good</td>', data)) == 0
    
    # Test that a super can be retrieved by name
    response = client.get(
        '/supers/',
        query_string = {
            'type': 'name',
            'hero': 'spiderman',
            'simple_regex': 'super',
            'regex': '[Ii]{3}'    
        }
    )
    assert response.status_code == 200
    data = str(response.data)
    assert len(re.findall(r'<img\s', data)) == 1
    assert len(re.findall(r'<td>Spider-Man</td>', data)) == 1
    assert len(re.findall(r'<td>Superman</td>', data)) == 0
    assert len(re.findall(r'<td>Black Knight III</td>', data)) == 0
    assert 'Hero Not Found' not in data
    
    # Test that a super can be retrieved by partial name
    response = client.get(
        '/supers/',
        query_string = {
            'type': 'simple_regex',
            'hero': 'spiderman',
            'simple_regex': 'super',
            'regex': '[Ii]{3}'    
        }
    )
    assert response.status_code == 200
    data = str(response.data)
    assert len(re.findall(r'<img\s', data)) == 5
    assert len(re.findall(r'<td>Spider-Man</td>', data)) == 0
    assert len(re.findall(r'<td>Superman</td>', data)) >= 1
    assert len(re.findall(r'<td>Black Knight III</td>', data)) == 0
    assert 'Hero Not Found' not in data
    
    # Test that a super can be retrieved by regex
    response = client.get(
        '/supers/',
        query_string = {
            'type': 'regex',
            'hero': 'spiderman',
            'simple_regex': 'super',
            'regex': '[Ii]{3}'    
        }
    )
    assert response.status_code == 200
    data = str(response.data)
    assert len(re.findall(r'<img\s', data)) == 5
    assert len(re.findall(r'<td>Spider-Man</td>', data)) == 0
    assert len(re.findall(r'<td>Superman</td>', data)) == 0
    assert len(re.findall(r'<td>Black Knight III</td>', data)) >= 1
    assert 'Hero Not Found' not in data
    
    #Test that the api properly handles no results
    response = client.get(
        '/supers/',
        query_string = {
            'type': 'name',
            'hero': 'doesnotexist',
            'simple_regex': 'doesnotexist',
            'regex': 'doesnotexist'    
        }
    )
    assert response.status_code == 200
    data = str(response.data)
    assert len(re.findall(r'<img\s', data)) == 0
    assert len(re.findall(r'<td>Spider-Man</td>', data)) == 0
    assert len(re.findall(r'<td>Superman</td>', data)) == 0
    assert len(re.findall(r'<td>Black Knight III</td>', data)) == 0
    assert 'Hero Not Found' in data
    
    #Test that the api properly handles the type being wrong
    response = client.get(
        '/supers/',
        query_string = {
            'type': 'bad',
            'hero': 'doesnotexist',
            'simple_regex': 'doesnotexist',
            'regex': 'doesnotexist'    
        }
    )
    assert response.status_code == 200
    data = str(response.data)
    assert len(re.findall(r'<img\s', data)) == 0
    assert len(re.findall(r'<td>Spider-Man</td>', data)) == 0
    assert len(re.findall(r'<td>Superman</td>', data)) == 0
    assert len(re.findall(r'<td>Black Knight III</td>', data)) == 0
    assert 'There was an error in parsing which type of query you are trying to make.' in data
