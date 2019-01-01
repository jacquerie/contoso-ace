import React from 'react';
import { Route } from 'react-router-dom';

import Chat from './Chat';
import Dashboard from './Dashboard';

class Chats extends React.Component {
  render() {
    const { match } = this.props;

    return (
      <div className="Chats">
        <Route path={match.path} exact component={Dashboard} />
        <Route path={`${match.path}/:id`} component={Chat} />
      </div>
    );
  }
}

export default Chats;
