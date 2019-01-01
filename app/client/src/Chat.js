import React from 'react';

class Chat extends React.Component {
  render() {
    const { match } = this.props;

    return (
      <div className="Chat">
        <h2>Chat #{match.params.id}</h2>
      </div>
    );
  }
}

export default Chat;
