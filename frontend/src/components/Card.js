import React from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

const Wrapper = styled.div`
    width: 530px;
    display: flex;
    flex-direction: column;
    border-radius: 10px;
    background-color: white;
    padding: 0 30px 20px 30px;
    margin: 8px 0;
`;

const Card = props => {
    return (
        <Wrapper>
            <h4>{props.user_name}</h4>
            <span>{props.text}</span>
        </Wrapper>
    );
};

Card.propTypes = {
    user_name: PropTypes.string,
    text: PropTypes.string
};

export default Card;