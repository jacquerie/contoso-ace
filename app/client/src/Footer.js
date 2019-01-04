import React from 'react';
import {
  Button,
  Container,
  Input,
  InputGroup,
  InputGroupAddon,
  Navbar,
} from 'reactstrap';

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

export default Footer;
