import PropTypes from 'prop-types';
import React from 'react';
import {
  Button,
  Card,
  CardBody,
  Col,
  Container,
  Form,
  FormGroup,
  Input,
  Label,
  Row,
} from 'reactstrap';

import './Login.css';

class Login extends React.Component {
  constructor(props) {
    super(props);

    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);

    fetch('/api/employees/login', {
      method: 'POST',
      credentials: 'same-origin',
      body: JSON.stringify({
        'email': formData.get('Email'),
        'password': formData.get('Password'),
      }),
    }).then(
      (response) => {
        if (response.ok) {
          this.context.router.history.push('/chats');
        }
      }
    );
  }

  render() {
    return (
      <div className="Login">
        <Container>
          <Row>
            <Col xs={{ offset: 3, size: 6 }}>
              <Card>
                <CardBody>
                  <Form onSubmit={this.handleSubmit}>
                    <FormGroup>
                      <Label for="Email">Email</Label>
                      <Input
                        type="email" name="Email" id="Email"
                        placeholder="barbara@contoso.com"
                      />
                    </FormGroup>
                    <FormGroup>
                      <Label for="Password">Password</Label>
                      <Input type="password" name="Password" id="Password" />
                    </FormGroup>
                    <Button type="submit" color="primary">Sign In</Button>
                  </Form>
                </CardBody>
              </Card>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

Login.contextTypes = {
  router: PropTypes.object.isRequired,
};

export default Login;
