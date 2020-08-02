import React from 'react';
import axios from 'axios';

class App extends React.Component {  
  constructor(props){
    super(props);    
    this.state = { radiant_score: 0, dire_score: 0, duration:0, result:'', k:3};
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

  kHandleChange = event => {
    event.preventDefault();
    this.setState({ k: event.target.value });
  };

  submitHandle = event => { 
    event.preventDefault();
    
    const match = {
      radiant_score: this.state.radiant_score,
      dire_score: this.state.dire_score,
      duration: this.state.duration,
      k: this.state.k
    };

    const url = `http://127.0.0.1:8080/api/predict`
    axios.post(url, null,{params:match})
      .then(res => {
        console.log(res);
        console.log(res.data);        
        this.setState({result:res.data.result})

      })
  };   
 
  render() {
    return (
      
      <React.Fragment >                
      <form onSubmit={this.submitHandle} style={{textAlign:"center", display:"block",alignContent:"center", backgroundColor:"black"}}>
          
          <input
            type="number"
            placeholder="Radiant  Score"
            name="radiant_score"            
            style={{borderColor: 'green', color: 'green'}}
            onChange={this.radiantHandleChange}
          />
          
          
          <input
            type="number"
            placeholder="Dire  Score"
            name="dire_score"            
            style={{borderColor: 'red', color: 'red'}}
            onChange={this.direHandleChange}
          />
          
          <input
            type="number"            
            placeholder="Duration -min 1200(s)- "
            name="duration"            
            min="1200"
            onChange={this.durationHandleChange}            
          />
          <p>
            <label style={{color:"white"}}>K=</label>
            <input
              type="number"            
              placeholder="K"
              defaultValue="3"
              name="k"            
              min="1"
              onChange={this.kHandleChange}    
            />
          </p>          
          <input type="submit" value="Predict" style={{ marginLeft: "auto" }}/>          
          {/* <h3 style={{color: 'white'}}>Result: {this.state.result}</h3> */}
        </form>        
        <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      }}> 
          <img alignContent="center" style={{width:"100%"}}  src={require('./data.png')}/>
        </div>
      </React.Fragment>      
    );
  }
 }
 export default App;

 const StyledForm = `
 width: 100%;
 max-width: 700px;
 padding: 40px;
 background-color: #fff;
 border-radius: 10px;
 box-sizing: border-box;
 box-shadow: 0px 0px 20px 0px rgba(0, 0, 0, 0.2);
`;