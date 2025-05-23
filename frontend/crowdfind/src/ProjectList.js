import React, {useState, useEffect} from 'react';

function ProjectList() {
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('https://my-backend.onrender.com/api/projects')
        .then(response => response.json())
        .then(data => {
            setProjects(data);
            setLoading(false);
        })
        .catch(error => console.error('Error:', error));
    }, []);

    if (loading) return <div>Loading Projects...</div>

    return (
        <div className="projects-container">
            <h1 className="projects-title">Projects</h1>
            <div className="projects-grid">
                {projects.map(project => (
                    <div key={project.id} className="project-card">
                        <div className="card-header">
                            <h2 className="project-name">{project.project_name}</h2>
                            <h3 className="company-title">{project.company_title}</h3>
                        </div>
                        
                        <div className="card-media">
                            <video 
                                src={project.project_picture_link} 
                                alt={project.project_name} 
                                className="project-video"
                                controls
                            />
                        </div>
                        
                        <div className="card-body">
                            <div className="profit-badge">
                                {project.estimated_profit}% پیش بینی سود
                            </div>
                            
                            <div className="project-details">
                                <p><strong>Platform:</strong> {project.crowdfunding_platform?.name}</p>
                                
                                <div className="feature-tags">
                                    <span className={`tag ${project.has_opportunity ? 'active' : ''}`}>
                                        {project.has_opportunity ? '✓ فرصت هست' : 'فرصت نیست'}
                                    </span>
                                    <span className={`tag ${project.has_warranty ? 'active' : ''}`}>
                                        {project.has_warranty ? '✓ ضمانت اصل سرمایه دارد' : 'ضمانت اصل سرمایه ندارد'}
                                    </span>
                                </div>
                            </div>
                        </div>
                        
                        <div className="card-footer">
                            <a href={project.telegram_link} className="telegram-link">
                                لینک تلگرام
                            </a>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ProjectList;