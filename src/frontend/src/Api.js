import React, {Component} from 'react';
import axios from 'axios'

class Result extends Component {
    state = {
        result: 0,
    };
    
    componentDidMount(){
        const url = 'http://183.120.120.3:8080/api/predict?radiant_score=1&dire_score=10&duration=5000'
        const params = {'radiant_score':'1','dire_score':'2','duration':'3'}
        axios.post(url).then(res => {
            console.log(res.data);
            this.setState({result:res.data.result});
        })
    }

    render() {
                let {result} = this.props;
                return (
                    <div className="result">                    
                        {this.state.result}
                    </div>
                    );
            }
}
export default Result;