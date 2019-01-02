import PropTypes from 'prop-types';
import React from 'react';
import { Container, Nav, NavItem, NavLink, Navbar } from 'reactstrap';

import './Header.css';

class Header extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      employee: null,
    };

    this.handleClick = this.handleClick.bind(this);
  }

  componentDidMount() {
    this.fetchEmployee();
  }

  fetchEmployee() {
    fetch('/api/employees/current', {
      'method': 'GET',
      'credentials': 'same-origin',
    }).then(
      response => response.ok ? response.json() : null
    ).then(
      json => this.setState({employee: json})
    )
  }

  handleClick(event) {
    event.preventDefault();

    fetch('/api/employees/logout', {
      'method': 'POST',
      'credentials': 'same-origin',
    }).then(
      response => response.ok ? null : this.state.employee
    ).then(
      json => this.setState({employee: json})
    ).then(
      () => this.context.router.history.push('/')
    )
  }

  render() {
    return (
      <div className="Header">
        <Navbar dark color="primary" expand="xs">
          <Container>
            <h1 className="navbar-text">Contoso ACE</h1>
            {this.state.employee !== null &&
              <Nav navbar>
                <NavItem className="navbar-text mr-3">
                  Hello, {this.state.employee.first_name}!
                </NavItem>
                <NavItem>
                  <NavLink onClick={this.handleClick}>
                    Sign Out
                  </NavLink>
                </NavItem>
              </Nav>
            }
          </Container>
        </Navbar>
      </div>
    );
  }
}

Header.contextTypes = {
  router: PropTypes.object.isRequired,
};

export default Header;
