import React from 'react';
import Timestamp from 'react-timestamp';
import {
  Badge,
  Button,
  Card,
  CardText,
  Col,
  Container,
  Input,
  InputGroup,
  InputGroupAddon,
  ListGroup,
  ListGroupItem,
  Navbar,
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

    this.fetchChat = this.fetchChat.bind(this);
    this.send = this.send.bind(this);
    this.predict = this.predict.bind(this);
  }

  componentDidMount() {
    this.timer = setInterval(() => this.fetchChat(), 1000);
  }

  componentWillUnmount() {
    clearInterval(this.timer);
  }

  fetchChat() {
    return fetch(`/api/chats/${this.state._id}`, {
      method: 'GET',
      credentials: 'same-origin',
    }).then(
      response => response.ok ? response.json() : {
        _id: this.state._id,
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

  send(text) {
    return fetch(`/api/chats/${this.state._id}/messages`, {
      method: 'POST',
      credentials: 'same-origin',
      body: JSON.stringify({text: text}),
    }).then(
      response => {
        if (response.ok) {
          this.setState({
            messages: this.state.messages.concat(response.json()),
          });
        }
      }
    );
  }

  predict() {
    return fetch(`/api/chats/${this.state._id}/predict`, {
      method: 'POST',
      credentials: 'same-origin',
    }).then(
      response => response.ok ? response.json() : {
        entities: this.state.entities,
        intent: this.state.intent,
      }
    ).then(
      json => this.setState({
        entities: json.entities,
        intent: json.intent,
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
        <Footer
          send={this.send}
          predict={this.predict}
        />
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
      {props.intent !== null && <Intent intent={props.intent} />}
      {props.entities.length > 0 && <Entities entities={props.entities} />}
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

class Footer extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      text: '',
    }

    this.handleSendChange = this.handleSendChange.bind(this);
    this.handleSendClick = this.handleSendClick.bind(this);
    this.handleSendKeyPress = this.handleSendKeyPress.bind(this);
    this.handlePredictClick = this.handlePredictClick.bind(this);
  }

  handleSendChange(event) {
    this.setState({text: event.target.value});
  }

  handleSendClick(event) {
    this.props.send(this.state.text).then(
      () => this.setState({text: ''})
    );
  }

  handleSendKeyPress(event) {
    if (event.key === 'Enter') {
      this.props.send(this.state.text).then(
        () => this.setState({'text': ''})
      );
    }
  }

  handlePredictClick(event) {
    this.props.predict();
  }

  render() {
    return (
      <div className="Footer">
        <Navbar dark color="primary" expand="xs" fixed="bottom">
          <Container>
            <InputGroup size="lg" className="mr-3">
              <Input
                type="text" value={this.state.text}
                onChange={this.handleSendChange}
                onKeyPress={this.handleSendKeyPress}
              />
              <InputGroupAddon addonType="append">
                <Button color="success" onClick={this.handleSendClick}>
                  Send
                </Button>
              </InputGroupAddon>
            </InputGroup>
            <Button color="danger" size="lg" onClick={this.handlePredictClick}>
              Predict
            </Button>
          </Container>
        </Navbar>
      </div>
    );
  }
}

export default Chat;
