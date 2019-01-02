import React from 'react';
import {
  Button,
  Card,
  CardBody,
  CardText,
  CardTitle,
  Col,
  Container,
  Row,
} from 'reactstrap';

import './Dashboard.css'

class Dashboard extends React.Component {
  render() {
    return (
      <div className="Dashboard">
        <Container>
          <Row>
            <Col xs="4">
              <Card>
                <CardBody>
                  <CardTitle tag="h2">Jane Doe</CardTitle>
                  <CardText>
                    Hi, I've got a trip to Paris next Monday
                    and I'd like to rent a car there.
                  </CardText>
                  <Button color="success">Accept</Button>
                </CardBody>
              </Card>
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

export default Dashboard;
