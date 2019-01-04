import PropTypes from 'prop-types';
import React from 'react';
import { Container, Nav, NavItem, NavLink, Navbar } from 'reactstrap';

import './Header.css';

class Header extends React.Component {
  constructor(props) {
    super(props);

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    this.props.logoutEmployee().then(
      () => this.context.router.history.push('/')
    );
  }

  render() {
    return (
      <div className="Header">
        <Navbar dark color="primary" expand="xs">
          <Container>
            <h1 className="navbar-text">Contoso ACE</h1>
            {this.props.employee !== null &&
              <Nav navbar>
                <NavItem className="navbar-text mr-3">
                  Hello, {this.props.employee.first_name}!
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
