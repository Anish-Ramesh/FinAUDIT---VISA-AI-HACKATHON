import ChatAssistant from '../components/ChatAssistant';
import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';

// Premium Palette Colors
const COLORS = {
    primary: '#6366f1',
    secondary: '#ec4899',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    info: '#06b6d4'
};
const CHART_COLORS = [COLORS.primary, COLORS.secondary, COLORS.success, COLORS.warning, COLORS.danger, COLORS.info];

const STANDARDS = [
    "General Transaction",
    "GDPR",
    "Visa CEDP",
    "AML / FATF",
    "PCI DSS",
    "Basel II / III"
];

const Dashboard = ({ data, onReset }) => {
    // Local state to handle re-evaluation updates
    const [dashboardData, setDashboardData] = useState(data);
    const [currentStandard, setCurrentStandard] = useState("General Transaction");
    const [isReanalyzing, setIsReanalyzing] = useState(false);
    const [isChatOpen, setIsChatOpen] = useState(false);

    useEffect(() => {
        setDashboardData(data);
        setCurrentStandard("General Transaction");
    }, [data]);

    const handleStandardChange = async (e) => {
        const newStandard = e.target.value;
        setCurrentStandard(newStandard);
        setIsReanalyzing(true);

        try {
            const response = await fetch('/api/analyze/re-evaluate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    metadata: dashboardData.metadata,
                    standard: newStandard
                })
            });

            if (!response.ok) throw new Error("Re-evaluation failed");

            const result = await response.json();

            // Merge new scores and analysis into dashboard data
            setDashboardData(prev => ({
                ...prev,
                scores: result.scores,
                analysis: result.analysis
            }));

        } catch (error) {
            console.error("Error switching standard:", error);
            alert("Failed to update compliance standard. See console.");
        } finally {
            setIsReanalyzing(false);
        }
    };

    const { scores, metadata, analysis, provenance } = dashboardData;

    // Transform dimension scores for chart
    const dimData = Object.keys(scores.dimension_scores).map(key => ({
        name: key.charAt(0).toUpperCase() + key.slice(1),
        score: scores.dimension_scores[key]
    }));

    const healthData = [
        { name: 'Health', value: scores.health_score },
        { name: 'Gap', value: 100 - scores.health_score }
    ];

    return (
        <>
            <div className="container animate-fade-in" style={{ paddingBottom: '6rem', maxWidth: '1400px', margin: '0 auto' }}>
                {/* Header Section */}
                <div className="flex-between" style={{ marginBottom: '2rem', borderBottom: '1px solid #e2e8f0', paddingBottom: '1rem', flexWrap: 'wrap', gap: '1rem' }}>
                    <div>
                        <h1 style={{ fontSize: '1.8rem', color: '#0f172a', marginBottom: '0.2rem' }}>Compliance Audit Report</h1>
                        <p style={{ fontSize: '0.9rem', color: '#64748b' }}>
                            Asset: <span style={{ color: COLORS.primary, fontWeight: 600, fontFamily: 'monospace' }}>{dashboardData.filename}</span>
                        </p>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                        {/* Compliance Selector */}
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <span style={{ fontSize: '0.9rem', fontWeight: 600, color: '#475569' }}>Standard:</span>
                            <select
                                value={currentStandard}
                                onChange={handleStandardChange}
                                disabled={isReanalyzing}
                                style={{
                                    padding: '0.5rem',
                                    borderRadius: '6px',
                                    border: '1px solid #cbd5e1',
                                    background: 'white',
                                    fontSize: '0.9rem',
                                    color: '#1e293b',
                                    cursor: 'pointer',
                                    minWidth: '180px'
                                }}
                            >
                                {STANDARDS.map(s => (
                                    <option key={s} value={s}>{s}</option>
                                ))}
                            </select>
                        </div>

                        <button onClick={onReset} className="btn btn-outline" style={{ background: 'white', padding: '0.5rem 1rem', fontSize: '0.9rem' }}>
                            <span>⚡</span> New Analysis
                        </button>
                    </div>
                </div>

                {/* Re-analysis Loading Overlay */}
                {isReanalyzing && (
                    <div style={{
                        position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                        background: 'rgba(255,255,255,0.7)',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        zIndex: 50, backdropFilter: 'blur(2px)'
                    }}>
                        <div className="card" style={{ padding: '2rem', textAlign: 'center' }}>
                            <div style={{ fontSize: '2rem', marginBottom: '1rem' }} className="animate-spin">🔄</div>
                            <h3 style={{ margin: 0 }}>Auditing against {currentStandard}...</h3>
                            <p style={{ margin: '0.5rem 0 0 0', color: '#64748b' }}>Running compliance rules engine.</p>
                        </div>
                    </div>
                )}

                {/* Attestation Banner */}
                {provenance && (
                    <div className="card" style={{
                        marginBottom: '2rem',
                        background: 'linear-gradient(to right, #f0fdf4, #ecfeff)',
                        borderColor: COLORS.success,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        padding: '1.5rem 2rem'
                    }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                            <span style={{ fontSize: '1.5rem' }}>🔒</span>
                            <div>
                                <h3 style={{ margin: 0, color: '#064e3b', fontSize: '1rem', fontWeight: 700 }}>VERIFIED AUDIT RECORD</h3>
                                <p style={{ margin: 0, color: '#065f46', fontSize: '0.9rem' }}>
                                    Hash Signed: {new Date(provenance.timestamp).toLocaleDateString()} {new Date(provenance.timestamp).toLocaleTimeString()}
                                </p>
                            </div>
                        </div>
                        <code style={{ background: 'white', padding: '0.5rem 1rem', borderRadius: '4px', fontSize: '0.8rem', color: '#059669', border: '1px solid #d1fae5' }}>
                            SHA256: {provenance.fingerprint.substring(0, 32)}...
                        </code>
                    </div>
                )}

                {/* AI Hero Section */}
                <div className="card" style={{
                    marginBottom: '2rem',
                    background: '#fff',
                    borderTop: `4px solid ${COLORS.primary}`,
                    boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
                }}>
                    <div className="flex-between" style={{ marginBottom: '1rem', borderBottom: '1px solid #f1f5f9', paddingBottom: '0.75rem' }}>
                        <h2 style={{ fontSize: '1.25rem', margin: 0, color: '#1e293b', fontWeight: 700 }}>Executive & Strategic Analysis ({currentStandard})</h2>
                        <div style={{ background: '#e0e7ff', color: COLORS.primary, padding: '0.25rem 0.75rem', borderRadius: '20px', fontSize: '0.7rem', fontWeight: 600 }}>
                            ✨ AI Advisory
                        </div>
                    </div>

                    {analysis.executive_summary ? (
                        <div style={{ display: 'grid', gridTemplateColumns: 'minmax(300px, 1fr) 1.5fr', gap: '2rem' }}>
                            {/* Left: Summary & Risk */}
                            <div>
                                <p style={{ fontSize: '1.05rem', lineHeight: '1.7', color: '#334155', marginBottom: '1.5rem' }}>
                                    {analysis.executive_summary}
                                </p>
                                <div style={{ background: '#fff1f2', padding: '1rem', borderRadius: '8px', border: '1px solid #ffe4e6' }}>
                                    <h4 style={{ color: '#991b1b', fontSize: '0.8rem', textTransform: 'uppercase', marginBottom: '0.5rem', fontWeight: 700 }}>Critical Risk Assessment</h4>
                                    <p style={{ margin: 0, color: '#7f1d1d', fontSize: '0.9rem', lineHeight: '1.5' }}>{analysis.risk_assessment}</p>
                                </div>
                            </div>

                            {/* Right: Scrollable Recommendations */}
                            <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                                <h4 style={{ color: '#475569', fontSize: '0.8rem', textTransform: 'uppercase', marginBottom: '0.75rem', fontWeight: 700 }}>Strategic Recommendations</h4>
                                <div style={{
                                    flex: 1,
                                    maxHeight: '300px',
                                    overflowY: 'auto',
                                    paddingRight: '0.5rem',
                                    display: 'grid',
                                    gap: '0.75rem',
                                    alignContent: 'start'
                                }} className="custom-scrollbar">
                                    {[...analysis.remediation_steps].sort((a, b) => (a.priority === 'CRITICAL' ? -1 : 1)).map((step, idx) => (
                                        <div key={idx} style={{
                                            display: 'flex',
                                            gap: '1rem',
                                            alignItems: 'baseline',
                                            padding: '0.75rem',
                                            background: '#f8fafc',
                                            borderRadius: '6px',
                                            borderLeft: step.priority === 'CRITICAL' ? '3px solid #ef4444' : '3px solid #e2e8f0'
                                        }}>
                                            <span style={{
                                                fontSize: '0.65rem',
                                                fontWeight: 'bold',
                                                padding: '0.15rem 0.4rem',
                                                borderRadius: '4px',
                                                background: step.priority === 'CRITICAL' ? '#fee2e2' : '#f1f5f9',
                                                color: step.priority === 'CRITICAL' ? '#991b1b' : '#64748b',
                                                minWidth: '60px',
                                                textAlign: 'center'
                                            }}>
                                                {step.priority || 'INFO'}
                                            </span>
                                            <div>
                                                <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#1e293b', marginBottom: '0.1rem' }}>{step.issue}</div>
                                                <div style={{ fontSize: '0.85rem', color: '#475569', lineHeight: '1.4' }}>{step.action}</div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div style={{ padding: '2rem', textAlign: 'center', color: '#94a3b8' }}>
                            <p>Analysis unavailable for this standard.</p>
                            <p style={{ fontSize: '0.8rem' }}>Try switching standards or uploading a new dataset.</p>
                        </div>
                    )}
                </div>

                {/* Metrics Row: Compact & Aligned */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.5rem', marginBottom: '2rem' }}>

                    {/* 1. Health Score (Compact) */}
                    <div className="card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '1.5rem' }}>
                        <div>
                            <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Overall Health</div>
                            <div style={{ fontSize: '2.5rem', fontWeight: 800, color: COLORS.primary, lineHeight: 1 }}>{scores.health_score}</div>
                            <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>/ 100 Score</div>
                        </div>
                        <div style={{ width: '80px', height: '80px' }}>
                            <ResponsiveContainer>
                                <PieChart>
                                    <Pie data={healthData} cx="50%" cy="50%" innerRadius={25} outerRadius={35} paddingAngle={0} dataKey="value" startAngle={90} endAngle={450}>
                                        <Cell fill={scores.health_score > 70 ? COLORS.success : COLORS.warning} />
                                        <Cell fill="#f1f5f9" />
                                    </Pie>
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* 2. Total Records */}
                    <div className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '1.5rem' }}>
                        <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Total Records</div>
                        <div style={{ fontSize: '2rem', fontWeight: 700, color: '#0f172a' }}>{metadata.total_rows.toLocaleString()}</div>
                    </div>

                    {/* 3. Column Count */}
                    <div className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '1.5rem' }}>
                        <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Active Columns</div>
                        <div style={{ fontSize: '2rem', fontWeight: 700, color: '#0f172a' }}>{metadata.total_columns}</div>
                    </div>

                    {/* 4. Rule Pass Rate */}
                    <div className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '1.5rem' }}>
                        <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Passed Rules</div>
                        <div style={{ fontSize: '2rem', fontWeight: 700, color: COLORS.success }}>
                            {Object.values(scores.rule_results).filter(r => r.passed).length}
                            <span style={{ fontSize: '1rem', color: '#cbd5e1', fontWeight: 400 }}>/{Object.keys(scores.rule_results).length}</span>
                        </div>
                    </div>
                </div>

                {/* Dimension Bar Chart (Full Width) */}
                <div className="card" style={{ marginBottom: '2rem', height: '300px', padding: '1.5rem' }}>
                    <h3 style={{ margin: '0 0 1.5rem 0', fontSize: '1rem', color: '#334155', fontWeight: 600 }}>Dimension Performance Breakdown</h3>
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={dimData} layout="vertical" margin={{ left: 80, right: 30, bottom: 20 }}>
                            <XAxis type="number" domain={[0, 100]} hide />
                            <YAxis
                                dataKey="name"
                                type="category"
                                width={100}
                                axisLine={false}
                                tickLine={false}
                                tick={{ fontSize: 13, fontWeight: 600, fill: '#475569', dx: -10 }}
                            />
                            <Tooltip
                                cursor={{ fill: '#f8fafc', opacity: 0.5 }}
                                contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)' }}
                            />
                            <Bar dataKey="score" radius={[0, 6, 6, 0]} barSize={24} animationDuration={1000}>
                                {dimData.map((e, i) => (
                                    <Cell key={i} fill={e.score > 80 ? COLORS.success : e.score > 50 ? COLORS.warning : COLORS.danger} />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Collapsible Details */}
                <div style={{ marginBottom: '4rem' }}>
                    <details style={{
                        background: 'white',
                        borderRadius: '12px',
                        border: '1px solid #e2e8f0',
                        overflow: 'hidden',
                        boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
                    }}>
                        <summary style={{
                            padding: '1.25rem 1.5rem',
                            cursor: 'pointer',
                            fontWeight: 600,
                            color: '#475569',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            listStyle: 'none',
                            background: '#f8fafc'
                        }} className="flex-between">
                            <span style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '1rem' }}>
                                📋 View Detailed Rule Logic & Scores ({currentStandard})
                            </span>
                            <span style={{ color: COLORS.primary, fontSize: '0.85rem' }}>View Table ▾</span>
                        </summary>

                        <div style={{ padding: '0 1.5rem 1.5rem 1.5rem', borderTop: '1px solid #e2e8f0' }}>
                            <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: '0' }}>
                                <thead>
                                    <tr style={{ color: '#94a3b8', fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                        <th style={{ textAlign: 'left', padding: '1rem 0', borderBottom: '1px solid #e2e8f0' }}>Rule Name</th>
                                        <th style={{ textAlign: 'center', padding: '1rem 0', borderBottom: '1px solid #e2e8f0' }}>Status</th>
                                        <th style={{ textAlign: 'right', padding: '1rem 0', borderBottom: '1px solid #e2e8f0' }}>Weight Score</th>
                                        <th style={{ textAlign: 'left', padding: '1rem 0 1rem 2rem', borderBottom: '1px solid #e2e8f0' }}>Audit Note</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {Object.entries(scores.rule_results).map(([key, result]) => (
                                        <tr key={key} style={{ fontSize: '0.9rem' }}>
                                            <td style={{ padding: '1rem 0', borderBottom: '1px solid #f1f5f9', fontWeight: 500, color: '#334155' }}>
                                                {key.replace(/_/g, ' ')}
                                            </td>
                                            <td style={{ padding: '1rem 0', textAlign: 'center', borderBottom: '1px solid #f1f5f9' }}>
                                                {result.passed ? (
                                                    <span style={{ color: '#166534', background: '#dcfce7', padding: '0.15rem 0.5rem', borderRadius: '12px', fontSize: '0.7rem', fontWeight: 700 }}>PASS</span>
                                                ) : (
                                                    <span style={{ color: '#991b1b', background: '#fee2e2', padding: '0.15rem 0.5rem', borderRadius: '12px', fontSize: '0.7rem', fontWeight: 700 }}>FAIL</span>
                                                )}
                                            </td>
                                            <td style={{ padding: '1rem 0', textAlign: 'right', borderBottom: '1px solid #f1f5f9', fontWeight: 600, color: result.score > 80 ? COLORS.success : COLORS.warning }}>
                                                {Math.round(result.score)}%
                                            </td>
                                            <td style={{ padding: '1rem 0 1rem 2rem', borderBottom: '1px solid #f1f5f9', color: '#64748b', fontSize: '0.85rem' }}>
                                                {result.details}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </details>
                </div>
            </div>

            {/* Floating Chat Button & Full Screen Modal - FIXED TO VIEWPORT */}
            <>
                {isChatOpen && (
                    <div className="animate-fade-in" style={{
                        position: 'fixed',
                        top: '5vh', left: '5vw', right: '5vw', bottom: '5vh',
                        background: 'rgba(255, 255, 255, 0.95)',
                        borderRadius: '24px',
                        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
                        border: '8px solid rgba(255, 255, 255, 0.3)',
                        backdropFilter: 'blur(8px)',
                        overflow: 'hidden',
                        display: 'flex',
                        flexDirection: 'column',
                        zIndex: 10000
                    }}>
                        <div style={{ padding: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #f1f5f9' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                <div style={{ fontSize: '2rem' }}>🤖</div>
                                <div>
                                    <h3 style={{ margin: 0, fontSize: '1.25rem', color: '#1e293b' }}>Compliance Assistant</h3>
                                    <p style={{ margin: 0, fontSize: '0.9rem', color: '#64748b' }}>Ask about dataset quality, risks, or remediation</p>
                                </div>
                            </div>
                            <button
                                onClick={() => setIsChatOpen(false)}
                                style={{
                                    border: 'none',
                                    background: '#f1f5f9',
                                    width: '40px',
                                    height: '40px',
                                    borderRadius: '50%',
                                    cursor: 'pointer',
                                    fontSize: '1.25rem',
                                    color: '#64748b',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center'
                                }}
                            >✕</button>
                        </div>

                        <div style={{ flex: 1, overflow: 'hidden', padding: '1rem' }}>
                            <ChatAssistant context={dashboardData} />
                        </div>
                    </div>
                )}

                <button
                    onClick={() => setIsChatOpen(!isChatOpen)}
                    style={{
                        position: 'fixed',
                        bottom: '30px',
                        right: '30px',
                        width: '70px',
                        height: '70px',
                        borderRadius: '50%',
                        background: COLORS.primary,
                        color: 'white',
                        border: '4px solid white',
                        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1)',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '2rem',
                        transition: 'transform 0.2s, box-shadow 0.2s',
                        zIndex: 9999
                    }}
                    onMouseEnter={e => {
                        e.target.style.transform = 'scale(1.1)';
                        e.target.style.boxShadow = '0 20px 25px -5px rgba(99, 102, 241, 0.4)';
                    }}
                    onMouseLeave={e => {
                        e.target.style.transform = 'scale(1)';
                        e.target.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.2)';
                    }}
                >
                    {isChatOpen ? '✕' : '💬'}
                </button>
            </>
        </>
    );
};

export default Dashboard;
