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
  constructor(props) {
    super(props);

    this.state = {
      chats: [],
    };
  }

  componentDidMount() {
    this.fetchChats();
  }

  fetchChats() {
    fetch('/api/chats', {
      'method': 'GET',
      'credentials': 'same-origin',
    }).then(
      response => response.json()
    ).then(
      json => this.setState({chats: json})
    )
  }

  toRows(chats) {
    let rows = [];

    for (let i = 0; i < chats.length; i = i + 3) {
      let cols = [];

      for (let j = i; j < chats.length && j < i + 3; j++) {
        cols.push(this.toCol(chats[j]));
      }

      rows.push(<Row>{cols}</Row>);
    }

    return <div className="Rows">{rows}</div>;
  }

  toCol(chat) {
    return (
      <Col xs="4">
        <Card>
          <CardBody>
            <CardTitle tag="h2">{chat.customer.full_name}</CardTitle>
            <CardText>{chat.message.text}</CardText>
            <Button color="success">Accept</Button>
          </CardBody>
        </Card>
      </Col>
    )
  }

  render() {
    return (
      <div className="Dashboard">
        <Container>
          {this.toRows(this.state.chats)}
        </Container>
      </div>
    );
  }
}

export default Dashboard;
