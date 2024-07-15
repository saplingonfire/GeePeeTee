import RenderPieChart from "../components/RenderPieChart.jsx";

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

    return (
        <>
            <div className='esg-scorecard'>
                <div id='company-details'>
                    <h1 id='company-details-title'>{companyScore.company} ESG Score</h1>
                    <h3 id='company-details-industry'>Industry: {companyScore.industry_code} {companyScore.industry}</h3>
                </div>
                <div>
                    <div className='align-left' id='scorecard-column-1'>
                        <h1>GeePeeTee ESG Score</h1>
                        <h1 id='esg_score'>{companyScore.total_score}</h1>
                        <p>Last Analyzed:<br/>{companyScore.timestamp}</p>
                    </div>
                    <div className='align-left' id='scorecard-column-2'>
                        <h1>Industry ESG Metric Breakdown</h1>
                        <h3> These are the ESG dimension weights particular to the industry: <br/>{companyScore.industry}</h3>
                        {RenderPieChart(dimension_weights)}
                    </div>
                    <div className='align-left' id='scorecard-column-3'>

                    </div>
                </div>
            </div>
        </>
    )
}

export default DetailedScorePage;