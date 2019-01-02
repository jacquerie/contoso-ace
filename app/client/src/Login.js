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
  render() {
    return (
      <div className="Login">
        <Container>
          <Row>
            <Col xs={{ offset: 3, size: 6 }}>
              <Card>
              <CardBody>
              <Form>
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
                <Button color="primary">Sign In</Button>
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

export default Login;
