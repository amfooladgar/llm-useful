from src.safety import validate_output
def test_validate_pass():
    validate_output({"score":0.5,"factors":["a"],"risks":["b"],"suggestions":[{"for":"initiator","text":"hi"},{"for":"recipient","text":"ok"}]})
