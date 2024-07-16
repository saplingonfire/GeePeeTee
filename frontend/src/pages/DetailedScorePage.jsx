import RenderPieChart from "../components/RenderPieChart.jsx";
import RenderGauge from "../components/RenderGauge.jsx";
import RenderBarCharts from "../components/RenderBarCharts.jsx";


function DetailedScorePage() {
    const companyScore = {
        company: 'Apple Inc',
        industry: 'Computers & Peripherals and Office Electronics',
        industry_code: 'THQ',
        total_score: 50,
        environmental: {score: 23, dimension_total: 35},
        social: {score: 14, dimension_total: 30},
        governance: {score: 13, dimension_total: 35},
        timestamp: '15-07-2024',
    }

    const dimension_weights = [
        { name: "Environmental", value: companyScore.environmental.dimension_total },
        { name: "Social", value: companyScore.social.dimension_total },
        { name: "Governance", value: companyScore.governance.dimension_total },
    ];

    const esg_score_category = [
        { name: 'Poor', value: 50, color: '#ff0000' },
        { name: 'Acceptable', value: 20, color: '#FF991F' },
        { name: 'Good', value: 30, color: '#88D65B' },
    ];

    // const dimension_scores = [
    //     { name: "Environmental", value: companyScore.environmental.score },
    //     { name: "Social", value: companyScore.social.score },
    //     { name: "Governance", value: companyScore.governance.score },
    // ];
    let esg_score_desc = '';
    if (companyScore.total_score <= 50) {
        esg_score_desc = 'Poor';
    } else if (companyScore.total_score >= 70) {
        esg_score_desc = 'Good';
    } else {
        esg_score_desc = 'Acceptable';
    };

    const bar_chart_data = [
        { 
            name: 'Environmental',
            "Score": companyScore.environmental.score,
            "out of": companyScore.environmental.dimension_total
        },
        { 
            name: 'Social',
            "Score": companyScore.social.score,
            "out of": companyScore.social.dimension_total
        },
        { 
            name: 'Governance',
            "Score": companyScore.governance.score,
            "out of": companyScore.governance.dimension_total
        }
    ];

    return (
        <>
            <div className='esg-scorecard'>
                <div id='company-details'>
                    <h1 id='company-details-title'>{companyScore.company} ESG Score</h1>
                    <div className='flex-row-space-between'>
                        <h3 id='company-details-industry'>Industry: {companyScore.industry_code} {companyScore.industry}</h3>
                        <a href='/'><button class='home-button'>{'< Back to Companies'}</button></a>
                    </div>
                </div>
                <div id='esg-score-details'>
                    <div className='align-left' id='scorecard-column-1'>
                        <h1>GeePeeTee ESG Score</h1>
                        <h1 class='text-no-margin' id='esg-score'>{companyScore.total_score}</h1>
                        <h1 class='text-no-margin'>{esg_score_desc}</h1>
                        {RenderGauge(esg_score_category, companyScore.total_score)}
                        <p>Last Analyzed:<br/>{companyScore.timestamp}</p>
                    </div>
                    <div className='align-left' id='scorecard-column-2'>
                        <h1>Industry ESG Dimension Breakdown</h1>
                        <h3> These are the ESG dimension weights particular to the industry: <br/>{companyScore.industry}</h3>
                        {RenderPieChart(dimension_weights)}
                    </div>
                    <div className='align-left' id='scorecard-column-3'>
                        <h1>ESG Score Breakdown</h1>
                        <h3>These are the company's scores in each ESG dimension</h3>
                        {RenderBarCharts(bar_chart_data)}
                    </div>
                </div>
            </div>
        </>
    )
}

export default DetailedScorePage;