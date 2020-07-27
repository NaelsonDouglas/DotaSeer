import React from 'react';
import { useForm } from 'react-hook-form';
import Result from './Result';
import axios from 'axios';




class App extends React.Component {

  constructor(props){
    super(props);
    this.state = { radiant_score: 0, dire_score: 0, duration:0, result:-1 };
  } 
 
  radiantHandleChange = event => {
    event.preventDefault();
    this.setState({ radiant_score: event.target.value });
  };

  direHandleChange = event => {
    event.preventDefault();
    this.setState({ dire_score: event.target.value });
  };

  durationHandleChange = event => {
    event.preventDefault();
    this.setState({ duration: event.target.value });
  };

  submitHandle = event => { 
    event.preventDefault();
    console.log("aaaaaaaaaaaa");
    this.setState({result:20})

  };   
 
  render() {
    return (
      <React.Fragment>
        <form onSubmit={this.submitHandle}>
          <label htmlFor="radiant_score">radiant_score</label>
          <input
            type="number"
            name="radiant_score"            
            onChange={this.radiantHandleChange}
          />

          <input
            type="number"
            name="dire_score"            
            onChange={this.direHandleChange}
          />

          <input
            type="number"
            name="duration"            
            onChange={this.durationHandleChange}
          />
          <input type="submit" value="Predict" style={{ marginLeft: "auto" }}/>
        </form> 
        <h3>Radiant score: {this.state.radiant_score}</h3>
        <h3>Radiant score: {this.state.dire_score}</h3>
        <h3>Duration: {this.state.duration}</h3>
        <h3>Result: {this.state.result}</h3>
      </React.Fragment>
    );
  }
 }
 export default App;


// import React from 'react';
// import { useForm } from 'react-hook-form';
// import Result from './Result';
// import axios from 'axios';



// export default function App() {
//   var dt = 10000000;  
//   const { register, handleSubmit } = useForm();
  
//   const onSubmit = data => {
//     console.log(data)    
//     const url = 'http://127.0.0.1:8080/api/predict?radiant_score=1&dire_score=10&duration=5000'
//     const params = {'radiant_score':'1','dire_score':'2','duration':'3'}
//     axios.post(url).then(res => {
//         console.log(res.data);
//         //this.dt=res.data.result
//         this.setState({result:res.data.result});
//     })
//   };   
 

//   return (    
//     <div style={{ display: "flex" }}>
//       <div>
//         <form onSubmit={handleSubmit(onSubmit)} >      
//             Radiant score:
//             <input name="radiant_score" defaultValue="0" ref={register} style={{ marginLeft: "right" }}/>
//             <div></div>
//             Dire score:
//             <input name="dire_score" defaultValue="0" ref={register} style={{ marginLeft: "right"}}/>
//             <div></div>
//             Duration:
//             <input name="duration" defaultValue="0" ref={register} style={{ marginLeft: "right" }}/>
//             <div></div>
//             <input type="submit" value="Predict" style={{ marginLeft: "auto" }}/>
//         </form>        
//         <Result result={dt}></Result>
//       </div>
//     </div>
//   );
// }