import React, { useState, useRef } from 'react';
import styled from 'styled-components'
import searchicon from '../search.svg';
import axios from 'axios';
import Card from "./Card";

const Wrapper = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center
`;

const FormContainer = styled.div`
    width: 400px;
    height: 70px;
    border-radius: 10px;
    background: white;
    box-shadow: 0 6px 30px -10px #d5dbed;
    margin-bottom: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
`;

const FormTab = styled.div`
    width: 95%;
    background: transparent;
    height: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
`

const SearchField = styled.div`
    width: 75%;
    height: 50px;
    background-color: #ECF1F4;
    border-radius: 6px;
    position: relative;
    overflow: hidden;
    z-index: 2;
`;

const SearchButton = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    text-transform: uppercase;
    cursor: pointer;
    width: 25%;
    z-index: 2;
`

const SearchIcon = styled.img`
    height: 40px;
    position: absolute;
    top: 5px;
    left: 8px;
`

const TextField = styled.input`
    background: transparent;
    font-size: 1.1em;
    color: #3f3f3f;
    border: none;
    width: 100%;
    height: 100%;
    padding: 5px 5px 5px 60px;
`

const PlaceHolder = styled.p`
    position: absolute;
    left: 60px;
    color: #6e80a5;
    opacity: 0.8;
`

const Form = styled.form`
    position: absolute;
    width: 100%;
    height: 100%;
`
const Overlay = styled.div`
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: ${props => props.active ? 1 : -1};
`

const Results = styled.div`
    display: flex;
    flex-direction: column;
`;

const Search = () => {
    const inputRef = useRef(null);

    const [active, setActive] = useState(false);
    const [query, setQuery] = useState("");
    const [results, setResults] = useState([]);

    const submitForm = async (e) => {
        e.preventDefault();
        const data = await axios.get("http://127.0.0.1:5000", {
            params: {
                q: query
            }
        })
        setActive(false);
        inputRef.current.blur();
        setResults(data.data);
    }

    return(
        <>
            <Overlay active={active} onClick={ () => { setActive(false) }  }/>
            <Wrapper >
                <FormContainer>
                    <FormTab onClick={() => { if(active) { setActive(false) } } }>
                        <SearchField onClick={(e) => { setActive(true); e.stopPropagation(); } }>
                            <SearchIcon src={searchicon}/>
                            {!active && query === "" ? <PlaceHolder>Documents</PlaceHolder> : <></>}
                            <Form onSubmit={submitForm}>
                                <TextField
                                    ref={inputRef}
                                    type={"text"}
                                    value={query}
                                    onChange={(e) => {
                                        const str = e.target.value.trim();
                                        if(!(query ==="" && str === ""))
                                            setQuery(e.target.value)
                                    }}
                                />
                            </Form>
                        </SearchField>
                        <SearchButton onClick={submitForm}>
                            <p>search</p>
                        </SearchButton>
                    </FormTab>
                </FormContainer>
                <Results>
                {
                    results.map( result =>
                        <Card
                            key={result.id}
                            text={result.text}
                            user_name={result.user_name}
                        />)
                }
                </Results>
            </Wrapper>
        </>
    )
}

export default Search;