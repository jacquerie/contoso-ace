import PropTypes from 'prop-types';
import React from 'react';
import {
  Button,
  Card,
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

    this.state = {
      email: '',
      password: '',
    };

    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleEmailChange(event) {
    this.setState({email: event.target.value});
  }

  handlePasswordChange(event) {
    this.setState({password: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();

    this.props.loginEmployee(
      this.state.email,
      this.state.password,
    ).then(
      () => this.context.router.history.push('/chats')
    );
  }

  render() {
    return (
      <div className="Login">
        <Container>
          <Row>
            <Col xs={{ offset: 3, size: 6 }}>
              <Card body>
                <Form onSubmit={this.handleSubmit}>
                  <FormGroup>
                    <Label for="Email">Email</Label>
                    <Input
                      type="email" name="Email" id="Email"
                      placeholder="barbara@contoso.com"
                      onChange={this.handleEmailChange}
                    />
                  </FormGroup>
                  <FormGroup>
                    <Label for="Password">Password</Label>
                    <Input type="password" name="Password" id="Password"
                      onChange={this.handlePasswordChange}
                    />
                  </FormGroup>
                  <Button type="submit" color="primary">Sign In</Button>
                </Form>
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
