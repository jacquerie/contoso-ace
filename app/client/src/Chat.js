import React from 'react';
import Timestamp from 'react-timestamp';
import {
  Badge,
  Card,
  CardText,
  Col,
  Container,
  ListGroup,
  ListGroupItem,
  Row,
} from 'reactstrap';

import './Chat.css';

class Chat extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      _id: this.props.match.params.id,
      customer: {},
      entities: [],
      intent: null,
      messages: [],
    };
  }

  componentDidMount() {
    this.timer = setInterval(() => this.fetchChat(this.state._id), 1000);
  }

  componentWillUnmount() {
    clearInterval(this.timer);
  }

  fetchChat(id) {
    return fetch(`/api/chats/${id}`, {
      method: 'GET',
      credentials: 'same-origin',
    }).then(
      response => response.ok ? response.json() : {
        _id: id,
        customer: {},
        entities: [],
        intent: null,
        messages: [],
      }
    ).then(
      json => this.setState({
        _id: json._id,
        customer: json.customer,
        entities: json.entities,
        intent: json.intent,
        messages: json.messages,
      })
    );
  }

  render() {
    return (
      <div className="Chat">
        <Container>
          <Row>
            <Col xs="8">
              <Messages
                customer={this.state.customer}
                messages={this.state.messages}
              />
            </Col>
            <Col xs={{ offset: 1, size: 3 }}>
              <Predictions
                entities={this.state.entities}
                intent={this.state.intent}
              />
            </Col>
          </Row>
        </Container>
      </div>
    );
  }
}

function Messages(props) {
  let messages = [];

  for (let i = 0; i < props.messages.length; i++) {
    messages.push(
      <Message
        customer={props.customer}
        message={props.messages[i]}
      />
    );
  }

  return <div className="Messages">{messages}</div>;
}

function Message(props) {
  if (props.message.sender === 'customer') {
    return (
      <div className="Message">
        <Row className="align-items-center h-100">
          <Col xs="4" className="text-center">
            <strong>{props.customer.first_name}</strong><br />
            <Timestamp
              time={props.message.timestamp / 1000} format='time'
            />
          </Col>
          <Col xs="8">
            <Card body outline color="primary">
              <CardText>{props.message.text}</CardText>
            </Card>
          </Col>
        </Row>
      </div>
    );
 } else {
    return (
      <div className="Message">
        <Row className="align-items-center h-100">
          <Col xs="8">
            <Card body outline color="secondary">
              <CardText>{props.message.text}</CardText>
            </Card>
          </Col>
          <Col xs="4" className="text-center">
            <strong>You</strong><br />
            <Timestamp
              time={props.message.timestamp / 1000} format='time'
            />
          </Col>
        </Row>
      </div>
    );
 }
}

function Predictions(props) {
  return (
    <div className="Predictions">
      <Intent intent={props.intent} />
      <Entities entities={props.entities} />
    </div>
  );
}

function Intent(props) {
  return (
    <div className="Intent">
      <h2>Intent</h2>
      <ListGroup>
        <ListGroupItem>{props.intent}</ListGroupItem>
      </ListGroup>
    </div>
  );
}

function Entities(props) {
  let entities = [];

  for (let i = 0; i < props.entities.length; i++) {
    entities.push(
      <ListGroupItem>
        <Badge color="primary" pill>{props.entities[i].type}</Badge>
        <span className="float-right">"{props.entities[i].snippet}"</span>
      </ListGroupItem>
    );
  }

  return (
    <div className="Entities">
      <h2>Entities</h2>
      <ListGroup>{entities}</ListGroup>
    </div>
  );
}

export default Chat;
