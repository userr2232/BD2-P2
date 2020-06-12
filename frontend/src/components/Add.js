import React, {Component} from 'react';
import styled from 'styled-components';
import axios from 'axios';

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
const SubmitButton = styled.button`
    display: flex;
    justify-content: center;
    align-items: center;
    text-transform: uppercase;
    cursor: pointer;
    width: 25%;
    z-index: 2;
`;


class Add extends Component{
    state = {
        isSelected: ""
    }
    fileSelectedHandler = event =>{
        this.setState({
            isSelected: event.target.files[0]
        })
        console.log(event.target.files[0]);
    }

    fileUploadHandler = () => {
        const new_data = new FormData();
        new_data.append('newFile', this.state.isSelected, this.state.isSelected.name);
        axios.post('http://127.0.0.1:5000/upload', {data: { filename: new_data}});
    }

    render() {
        return (
        <Wrapper>
            <form method="post" >
                <input name="newfile" type="file" onChange={this.fileSelectedHandler}/>
                <button type="submit">submit</button>
            </form>
        </Wrapper>
        );
    }
}
export default Add;