import React from 'react';
import { useForm } from 'react-hook-form';
import Result from './Result';
import axios from 'axios';



export default function App() {
  var dt = 10000000;  
  const { register, handleSubmit } = useForm();
  
  const onSubmit = data => {
    console.log(data)    
    const url = 'http://127.0.0.1:8080/api/predict?radiant_score=1&dire_score=10&duration=5000'
    const params = {'radiant_score':'1','dire_score':'2','duration':'3'}
    axios.post(url).then(res => {
        console.log(res.data);
        //this.dt=res.data.result
        this.setState({result:res.data.result});
    })
  };   
 

  return (    
    <div style={{ display: "flex" }}>
      <div>
        <form onSubmit={handleSubmit(onSubmit)} >      
            Radiant score:
            <input name="radiant_score" defaultValue="0" ref={register} style={{ marginLeft: "right" }}/>
            <div></div>
            Dire score:
            <input name="dire_score" defaultValue="0" ref={register} style={{ marginLeft: "right"}}/>
            <div></div>
            Duration:
            <input name="duration" defaultValue="0" ref={register} style={{ marginLeft: "right" }}/>
            <div></div>
            <input type="submit" value="Predict" style={{ marginLeft: "auto" }}/>
        </form>        
        <Result result={dt}></Result>
      </div>
    </div>
  );
}