import React from 'react';
import styled from 'styled-components';
import Search from "./components/Search";

const Wrapper = styled.div`
    background: #f1f3f9;
    width: 100vw;
    min-height: 100vh;
    overflow: auto;
    display: flex;
    justify-content: center;
    padding: 60px 0;
`

function App() {
  return (
    <Wrapper>
      <Search/>
    </Wrapper>
  );
}

export default App;
