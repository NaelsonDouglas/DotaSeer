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

    const url = `http://35.225.42.57:8080/api/predict`
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
      <p>
            <label style={{color:"white"}}>Dota is a 5v5 online game where two teams, Radiant(green) and Dire(red) fight one against the other to destroy the rival building  named 'ancient'.</label>            
            <p><label style={{color:"white"}}>Each team must defend their ancient, therefore, they are called Defenders of the Ancients(DOTA)</label></p>
            <p><label style={{color:"white"}}>When a player from the Dire team dies, Radiant scores one point and the same happens to Dire when a member of the Radiant team dies.</label></p>
            <p><label style={{color:"white"}}>It's quite obvious to say a team with bigger score has more chances to win, but there's a popular say among Dota players where it's said 'score doesn't matter on long matches'. That's because on long matches, each team is already playing on the highest level, so killing more or less  doesnt  inflict  such big difference.</label></p>
            <p><label style={{color:"white"}}>This predictor uses 3 variables Radiant Score, Team Score and Match duration(s) to predict  which team wins  given the situation.</label></p>
      </p>
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
          <input type="submit" value="Predict" style={{ marginLeft: "auto",padding:"15px 90px", cursor:"pointer"}}/>          
          <br></br>
          -
          
          {/* <h3 style={{color: 'white'}}>Result: {this.state.result}</h3> */}
        </form>        
        <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      }}> 
          <img alignContent="center" style={{width:"80%"}} alt="Data plot" src={require('./plot/plot.png')}/>
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