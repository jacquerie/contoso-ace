import PropTypes from 'prop-types';
import React from 'react';
import { CircleSpinner } from 'react-spinners-kit';
import {
  Button,
  Card,
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
      loading: true,
    };

    this.handleClick = this.handleClick.bind(this);
  }

  componentDidMount() {
    this.timer = setInterval(() => this.fetchChats(), 1000);
  }

  componentWillUnmount() {
    clearInterval(this.timer);
  }

  fetchChats() {
    fetch('/api/chats', {
      'method': 'GET',
      'credentials': 'same-origin',
    }).then(
      response => response.ok ? response.json() : []
    ).then(
      json => this.setState({chats: json})
    ).then(
      () => this.setState({loading: false})
    );
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
        <Card body>
          <CardTitle tag="h2">{chat.customer.full_name}</CardTitle>
          <CardText>{chat.message.text}</CardText>
          <Button onClick={() => this.handleClick(chat._id)}
            color="success">
            Accept
          </Button>
        </Card>
      </Col>
    )
  }

  handleClick(id) {
    fetch(`/api/chats/${id}/employees`, {
      method: 'POST',
      credentials: 'same-origin',
    }).then(
      response => {
        if (response.ok) {
          this.context.router.history.push(`/chats/${id}`);
        }
      }
    )
  }

  render() {
    return (
      <div className="Dashboard">
        <Container>
          {this.state.loading ? (
            <div className="d-flex flex-wrap justify-content-center">
              <CircleSpinner color="#0077ff" size="96" />
            </div>
          ) : (
            this.toRows(this.state.chats)
          )}
        </Container>
      </div>
    );
  }
}

Dashboard.contextTypes = {
  router: PropTypes.object.isRequired,
};

export default Dashboard;
