import streamlit as st
import streamlit.components.v1 as components

# Set up page configurations with macOS design tokens
st.set_page_config(
    page_title="Timeline Workspace",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide default Streamlit header/footer padding for absolute native desktop app feel
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Main container containing the interactive macOS Workspace
html_app = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Timeline Workspace</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.3/babel.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class'
    }
  </script>
  <style>
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: transparent;
    }
    ::-webkit-scrollbar-thumb {
      background: #3f3f46;
      border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #52525b;
    }
  </style>
</head>
<body class="bg-zinc-50 dark:bg-[#09090b] text-zinc-900 dark:text-zinc-50 transition-colors duration-300 antialiased overflow-x-hidden">
  <div id="root"></div>

  <script type="text/babel">
    const { useState, useEffect } = React;

    // Class Merger Helper
    const cn = (...classes) => classes.filter(Boolean).join(' ');

    // Inline SVG Icon primitives for performance & consistency
    const SunIcon = () => <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m0 13.5V21M4.22 4.22l1.59 1.59m12.38 12.38l1.59 1.59M3 12h2.25m13.5 0H21M4.22 19.78l1.59-1.59m12.38-12.38l1.59-1.59M12 7.5a4.5 4.5 0 110 9 4.5 4.5 0 010-9z" /></svg>;
    const MoonIcon = () => <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" /></svg>;
    const PlusIcon = () => <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>;
    const CheckIcon = ({ className = "w-4 h-4" }) => <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="3"><path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" /></svg>;
    const TrashIcon = ({ className = "w-3.5 h-3.5" }) => <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M14.74 9l-.34 9m-4.78 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" /></svg>;
    const XIcon = ({ className = "w-4 h-4" }) => <svg className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>;
    const FolderIcon = () => <svg className="w-4 h-4 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12.75V12A2.25 2.25 0 014.5 9.75h15A2.25 2.25 0 0123.75 12v.75m-21.5 0A2.25 2.25 0 004.5 15h15a2.25 2.25 0 002.25-2.25m-21.5 0v3A2.25 2.25 0 004.5 18h15a2.25 2.25 0 002.25-2.25v-3m-19.5-6h3.456a1.875 1.875 0 011.196.425l1.258 1.006a1.875 1.875 0 001.196.425H21.75" /></svg>;
    const FolderPlusIcon = () => <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M12 10.5v6m3-3H9m4.056-11.544l.426.213a1.875 1.875 0 011.196.425l1.258 1.006a1.875 1.875 0 001.196.425h4.124A1.875 1.875 0 0124 10.125V18.375c0 1.036-.84 1.875-1.875 1.875H3.875A1.875 1.875 0 012 18.375V6.75c0-1.036.84-1.875 1.875-1.875h3.456a1.875 1.875 0 011.196.425l1.258 1.006a1.875 1.875 0 001.196.425h4.124z" /></svg>;
    const ArrowUpRightIcon = () => <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25" /></svg>;
    const EditIcon = () => <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" /></svg>;
    const CalendarIcon = () => <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" /></svg>;

    // Curated Milestones icons
    const FlagIcon = () => <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M3 3v1.5M3 21v-6m0 0l2.77-.693a9 9 0 016.208.682l.108.054a9 9 0 006.086.71l3.114-.732a1.125 1.125 0 00.732-1.025V4.5a1.125 1.125 0 00-1.463-1.07l-3.328.892a9 9 0 01-6.185-.64l-.108-.054a9 9 0 00-6.143-.65L3 4.5m0 10.5V4.5" /></svg>;
    const StarIcon = () => <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M11.48 3.499c.178-.393.73-.393.908 0l2.316 5.111 5.378.363c.435.03.608.567.283.856l-3.992 3.553 1.18 5.257c.095.424-.363.757-.733.528l-4.757-2.955-4.757 2.955c-.37.229-.828-.104-.733-.528l1.18-5.257-3.992-3.553c-.325-.289-.152-.826.283-.856l5.378-.363 2.316-5.111z" /></svg>;
    const RocketIcon = () => <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M15.59 14.37a6 6 0 01-5.84 7.38v-4.8m5.84-2.58a14.98 14.98 0 006.16-12.12A14.98 14.98 0 009.63 8.41a14.98 14.98 0 00-6.16 12.12A14.98 14.98 0 0015.59 14.37z" /></svg>;
    const CodeIcon = () => <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M17.25 6.75L22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3l-4.5 16.5" /></svg>;
    const PaletteIcon = () => <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M9.53 16.122a3 3 0 00-2.225.163l-.337.168a3 3 0 01-2.225.163l-.337-.168a3 3 0 00-2.225.163L2 16.737V21h15v-4.878l-7.47-4.878zM22 6.75L12 11.25l-2.25-2.25L19.75 4.5 22 6.75z" /></svg>;
    const SearchIcon = () => <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.637 10.637z" /></svg>;
    const SparklesIcon = () => <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 21l-.813-5.096L3 15l5.187-.813L9 9l.813 5.187L15 15l-5.187.904zM19.071 4.929l-.353 1.768-1.768.353 1.768.353.353 1.768.353-1.768 1.768-.353-1.768-.353-.353-1.768z" /></svg>;
    const TrophyIcon = () => <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M16.5 18.75h-9m9 0a3 3 0 013 3h-15a3 3 0 013-3m9 0v-3.375c0-.621-.504-1.125-1.125-1.125h-6.75A1.125 1.125 0 007.5 15.375V18.75M9 3.75h6m-12 3a3 3 0 003 3h12a3 3 0 003-3v-1.5a3 3 0 00-3-3H6a3 3 0 00-3 3v1.5z" /></svg>;
    const TargetIcon = () => <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M12 3v18m9-9H3m12 0a3 3 0 11-6 0 3 3 0 016 0z" /></svg>;

    // Curated Milestones list mapped correctly
    const AVAILABLE_ICONS = [
      { name: 'number', label: '#' },
      { name: 'flag', icon: FlagIcon },
      { name: 'star', icon: StarIcon },
      { name: 'rocket', icon: RocketIcon },
      { name: 'code', icon: CodeIcon },
      { name: 'palette', icon: PaletteIcon },
      { name: 'search', icon: SearchIcon },
      { name: 'sparkles', icon: SparklesIcon },
      { name: 'trophy', icon: TrophyIcon },
      { name: 'target', icon: TargetIcon },
    ];

    const renderCheckpointIcon = (iconName, index) => {
      switch (iconName) {
        case 'flag': return <FlagIcon />;
        case 'star': return <StarIcon />;
        case 'rocket': return <RocketIcon />;
        case 'code': return <CodeIcon />;
        case 'palette': return <PaletteIcon />;
        case 'search': return <SearchIcon />;
        case 'sparkles': return <SparklesIcon />;
        case 'trophy': return <TrophyIcon />;
        case 'target': return <TargetIcon />;
        default: return <span className="font-bold font-mono text-xs">{index + 1}</span>;
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return '';
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    };

    // UI primitives setup
    const Button = ({ className = '', variant = 'default', ...props }) => {
      const baseStyles = 'inline-flex items-center justify-center rounded-md text-xs font-semibold tracking-tight transition-all duration-200 disabled:opacity-50 select-none active:scale-[0.98] h-9 px-4 py-2';
      const variants = {
        default: 'bg-zinc-900 text-zinc-50 hover:bg-zinc-800 dark:bg-zinc-100 dark:text-zinc-950 dark:hover:bg-zinc-200',
        outline: 'border border-zinc-200 bg-white hover:bg-zinc-50 hover:text-zinc-900 dark:border-zinc-800 dark:bg-zinc-950 dark:hover:bg-zinc-900 dark:hover:text-zinc-50',
        secondary: 'bg-zinc-100 text-zinc-900 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-50 dark:hover:bg-zinc-700',
      };
      return <button className={`${baseStyles} ${variants[variant]} ${className}`} {...props} />;
    };

    const Input = ({ className = '', ...props }) => (
      <input className={`flex h-9 w-full rounded-md border border-zinc-200 bg-zinc-50/30 px-3 py-1 text-sm shadow-2xs transition-all placeholder:text-zinc-400 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-zinc-900/50 dark:border-zinc-800 dark:bg-zinc-950/20 dark:placeholder:text-zinc-600 dark:focus-visible:ring-zinc-450 ${className}`} {...props} />
    );

    const Textarea = ({ className = '', ...props }) => (
      <textarea className={`flex min-h-[60px] w-full rounded-md border border-zinc-200 bg-zinc-50/30 px-3 py-2 text-sm shadow-2xs placeholder:text-zinc-400 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-zinc-900/50 dark:border-zinc-800 dark:bg-zinc-950/20 dark:placeholder:text-zinc-600 dark:focus-visible:ring-zinc-450 ${className}`} {...props} />
    );

    const Card = ({ className = '', ...props }) => (
      <div className={`rounded-xl border border-zinc-200 bg-white text-zinc-955 shadow-xs dark:border-zinc-800/60 dark:bg-zinc-950 dark:text-zinc-50 transition-all duration-350 ${className}`} {...props} />
    );

    const Badge = ({ className = '', ...props }) => (
      <div className={`inline-flex items-center rounded-full border border-transparent bg-zinc-100 text-zinc-900 dark:bg-zinc-900 dark:text-zinc-300 px-2.5 py-0.5 text-[10px] font-bold tracking-wider uppercase ${className}`} {...props} />
    );

    // ==========================================
    // Seed Data Setup
    // ==========================================
    const SEED_DATA = [
      {
        id: "proj-1",
        title: "Guidance from industry leaders",
        description: "A curated roadmap designed to take your venture from a raw concept to a successful market launch.",
        pendingTasks: [
          { id: "pt-1", text: "Brand Identity Strategy" },
          { id: "pt-2", text: "Beta Analytics Integration" }
        ],
        checkpoints: [
          {
            id: "cp-1",
            title: "Ideation",
            headline: "Brainstorm and validate your concept",
            subtitle: "~2 weeks",
            description: "Gather insights from market research, customer interviews, and competitor analysis to refine your product idea.",
            icon: "search",
            deadline: "2026-05-30",
            checklist: [
              { id: "t-1", text: "Market research & insights", isCompleted: true },
              { id: "t-2", text: "Competitor analysis", isCompleted: false },
              { id: "t-3", text: "Define value proposition", isCompleted: false }
            ]
          },
          {
            id: "cp-2",
            title: "Development",
            headline: "Build your MVP",
            subtitle: "~6 weeks",
            description: "Design, prototype, and develop the minimum viable product. Iterate quickly based on early feedback and testing.",
            icon: "code",
            deadline: "2026-07-15",
            checklist: [
              { id: "t-4", text: "Draft wireframes", isCompleted: true },
              { id: "t-5", text: "Set up database schema", isCompleted: true },
              { id: "t-6", text: "Develop core functionality", isCompleted: false }
            ]
          }
        ]
      }
    ];

    function App() {
      const [isDarkMode, setIsDarkMode] = useState(true);
      const [projects, setProjects] = useState([]);
      const [activeProjectId, setActiveProjectId] = useState(null);
      const [selectedCheckpointId, setSelectedCheckpointId] = useState(null);

      const [quickTaskText, setQuickTaskText] = useState('');
      const [modalNewTaskText, setModalNewTaskText] = useState('');

      useEffect(() => {
        const rootHtml = document.documentElement;
        if (isDarkMode) {
          rootHtml.classList.add('dark');
        } else {
          rootHtml.classList.remove('dark');
        }
      }, [isDarkMode]);

      // Read local state from localStorage inside standard iframe stream
      useEffect(() => {
        const local = localStorage.getItem("timeline_projects");
        if (local) {
          try {
            const parsed = JSON.parse(local);
            setProjects(parsed);
            if (parsed.length > 0) setActiveProjectId(parsed[0].id);
          } catch (e) {
            setProjects(SEED_DATA);
            setActiveProjectId(SEED_DATA[0].id);
          }
        } else {
          setProjects(SEED_DATA);
          setActiveProjectId(SEED_DATA[0].id);
          localStorage.setItem("timeline_projects", JSON.stringify(SEED_DATA));
        }
      }, []);

      const saveToLocal = (newProjects) => {
        setProjects(newProjects);
        localStorage.setItem("timeline_projects", JSON.stringify(newProjects));
      };

      const activeProject = projects.find(p => p.id === activeProjectId) || projects[0] || {
        id: '',
        title: 'Initialising App...',
        description: '',
        pendingTasks: [],
        checkpoints: []
      };

      const activeCheckpoint = (activeProject.checkpoints || []).find(cp => cp.id === selectedCheckpointId);

      const handleCreateProject = () => {
        const newProj = {
          id: `proj-${Date.now()}`,
          title: 'New Project Roadmap',
          description: 'Describe your new project goals here.',
          pendingTasks: [],
          checkpoints: []
        };
        saveToLocal([...projects, newProj]);
        setActiveProjectId(newProj.id);
      };

      const handleDeleteProject = (projectId, e) => {
        e.stopPropagation();
        if (projects.length <= 1) return;
        const remaining = projects.filter(p => p.id !== projectId);
        saveToLocal(remaining);
        setActiveProjectId(remaining[0].id);
      };

      const handleUpdateProjectMeta = (field, value) => {
        if (!activeProject.id) return;
        const updatedProjects = projects.map(p => {
          if (p.id === activeProject.id) {
            return { ...p, [field]: value };
          }
          return p;
        });
        saveToLocal(updatedProjects);
      };

      const handleAddQuickTask = (e) => {
        e.preventDefault();
        if (!quickTaskText.trim() || !activeProject.id) return;
        const newTask = { id: `pt-${Date.now()}`, text: quickTaskText.trim() };
        const updatedProjects = projects.map(p => {
          if (p.id === activeProject.id) {
            return { ...p, pendingTasks: [...(p.pendingTasks || []), newTask] };
          }
          return p;
        });
        saveToLocal(updatedProjects);
        setQuickTaskText('');
      };

      const handleDeleteQuickTask = (taskId) => {
        if (!activeProject.id) return;
        const updatedProjects = projects.map(p => {
          if (p.id === activeProject.id) {
            return { ...p, pendingTasks: (p.pendingTasks || []).filter(t => t.id !== taskId) };
          }
          return p;
        });
        saveToLocal(updatedProjects);
      };

      const handleConvertTaskToCheckpoint = (task) => {
        if (!activeProject.id) return;
        const newCheckpoint = {
          id: `cp-${Date.now()}`,
          title: task.text,
          headline: '',
          subtitle: '',
          description: '',
          icon: 'number',
          deadline: '',
          checklist: []
        };
        const updatedProjects = projects.map(p => {
          if (p.id === activeProject.id) {
            return {
              ...p,
              pendingTasks: (p.pendingTasks || []).filter(t => t.id !== task.id),
              checkpoints: [...(p.checkpoints || []), newCheckpoint]
            };
          }
          return p;
        });
        saveToLocal(updatedProjects);
      };

      const handleUpdateCheckpointDetail = (checkpointId, field, value) => {
        if (!activeProject.id) return;
        const updatedProjects = projects.map(p => {
          if (p.id === activeProject.id) {
            return {
              ...p,
              checkpoints: (p.checkpoints || []).map(cp => 
                cp.id === checkpointId ? { ...cp, [field]: value } : cp
              )
            };
          }
          return p;
        });
        saveToLocal(updatedProjects);
      };

      const handleAddModalChecklistItem = (checkpointId, e) => {
        e.preventDefault();
        if (!modalNewTaskText.trim() || !activeProject.id) return;
        const newItem = { id: `t-${Date.now()}`, text: modalNewTaskText.trim(), isCompleted: false };
        const updatedProjects = projects.map(p => {
          if (p.id === activeProject.id) {
            return {
              ...p,
              checkpoints: (p.checkpoints || []).map(cp => {
                if (cp.id === checkpointId) {
                  return { ...cp, checklist: [...(cp.checklist || []), newItem] };
                }
                return cp;
              })
            };
          }
          return p;
        });
        saveToLocal(updatedProjects);
        setModalNewTaskText('');
      };

      const handleToggleTask = (checkpointId, taskId) => {
        if (!activeProject.id) return;
        const updatedProjects = projects.map(p => {
          if (p.id === activeProject.id) {
            return {
              ...p,
              checkpoints: (p.checkpoints || []).map(cp => {
                if (cp.id === checkpointId) {
                  return {
                    ...cp,
                    checklist: (cp.checklist || []).map(t => t.id === taskId ? { ...t, isCompleted: !t.isCompleted } : t)
                  };
                }
                return cp;
              })
            };
          }
          return p;
        });
        saveToLocal(updatedProjects);
      };

      const handleRemoveModalChecklistItem = (checkpointId, taskId) => {
        if (!activeProject.id) return;
        const updatedProjects = projects.map(p => {
          if (p.id === activeProject.id) {
            return {
              ...p,
              checkpoints: (p.checkpoints || []).map(cp => {
                if (cp.id === checkpointId) {
                  return { ...cp, checklist: (cp.checklist || []).filter(t => t.id !== taskId) };
                }
                return cp;
              })
            };
          }
          return p;
        });
        saveToLocal(updatedProjects);
      };

      const handleRemoveCheckpoint = (checkpointId, e) => {
        e.stopPropagation();
        if (!activeProject.id) return;
        const updatedProjects = projects.map(p => {
          if (p.id === activeProject.id) {
            return {
              ...p,
              checkpoints: (p.checkpoints || []).filter(cp => cp.id !== checkpointId)
            };
          }
          return p;
        });
        saveToLocal(updatedProjects);
        if (selectedCheckpointId === checkpointId) {
          setSelectedCheckpointId(null);
        }
      };

      return (
        <div className="min-h-screen pb-24 font-sans">
          {/* macOS titlebar header design mock - Traffic lights removed & expanded to full width */}
          <header className="border-b border-zinc-200 dark:border-zinc-900 bg-white/90 dark:bg-zinc-950/90 sticky top-0 backdrop-blur-lg z-40 px-6 md:px-12 py-4">
            <div className="w-full flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="font-extrabold text-xs tracking-widest uppercase text-zinc-500 dark:text-zinc-400">Timeline Workspace</span>
              </div>
              <Button variant="outline" className="w-8 h-8 rounded-lg !p-0" onClick={() => setIsDarkMode(!isDarkMode)}>
                {isDarkMode ? <SunIcon /> : <MoonIcon />}
              </Button>
            </div>
          </header>

          <main className="w-full px-6 md:px-12 pt-10 space-y-8 animate-in fade-in duration-300">
            {/* Project Index list */}
            <Card className="p-6">
              <div className="flex items-center justify-between mb-4 pb-2 border-b border-zinc-100 dark:border-zinc-900">
                <div className="flex items-center gap-2">
                  <FolderIcon />
                  <h2 className="text-[10px] font-bold tracking-widest uppercase text-zinc-400">Project Index</h2>
                </div>
                <Button variant="outline" onClick={handleCreateProject} className="gap-1.5 h-7 rounded-sm border-dashed text-[11px] !px-2.5">
                  <FolderPlusIcon /> Create New
                </Button>
              </div>

              <div className="flex flex-wrap gap-1.5">
                {projects.map(p => {
                  const isActive = p.id === activeProjectId;
                  return (
                    <div
                      key={p.id}
                      onClick={() => { setActiveProjectId(p.id); setSelectedCheckpointId(null); }}
                      className={`group relative flex items-center gap-2.5 px-3 py-1.5 rounded-sm border text-[11px] font-bold tracking-tight cursor-pointer transition-all duration-200 ${
                        isActive 
                          ? 'bg-zinc-900 text-zinc-50 border-transparent dark:bg-zinc-100 dark:text-zinc-950'
                          : 'bg-zinc-100/30 border-zinc-200 text-zinc-500 dark:bg-zinc-900/35 dark:border-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-900/70'
                      }`}
                    >
                      <span className="truncate max-w-[160px]">{p.title}</span>
                      {projects.length > 1 && (
                        <button onClick={(e) => handleDeleteProject(p.id, e)} className="opacity-0 group-hover:opacity-100 p-0.5 text-zinc-400 hover:text-red-500">
                          <TrashIcon />
                        </button>
                      )}
                    </div>
                  );
                })}
              </div>
            </Card>

            {/* Config metadata fields and Quick Tasks */}
            <Card className="overflow-hidden">
              <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-zinc-100 dark:divide-zinc-900">
                
                <div className="p-6 space-y-5">
                  <h2 className="text-[10px] font-bold tracking-widest uppercase text-zinc-400">Settings</h2>
                  <div className="space-y-4">
                    <div className="space-y-1.5">
                      <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-500">Header / Brand text</label>
                      <Input type="text" value={activeProject.title || ''} onChange={e => handleUpdateProjectMeta('title', e.target.value)} className="h-8 rounded-sm text-xs font-semibold" />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-500">Description Summary</label>
                      <Textarea value={activeProject.description || ''} onChange={e => handleUpdateProjectMeta('description', e.target.value)} className="min-h-[80px] resize-none rounded-sm text-xs leading-relaxed" />
                    </div>
                  </div>
                </div>

                <div className="p-6 flex flex-col justify-between space-y-5">
                  <div className="space-y-4">
                    <div className="space-y-1">
                      <h2 className="text-[10px] font-bold tracking-widest uppercase text-zinc-400">Tasks Pool</h2>
                      <p className="text-[11px] text-zinc-500 mt-0.5">Add checklist phases, then convert them into checkpoints.</p>
                    </div>
                    <form onSubmit={handleAddQuickTask} className="flex gap-1.5">
                      <Input type="text" required value={quickTaskText} onChange={e => setQuickTaskText(e.target.value)} placeholder="e.g., Wireframe layout" className="h-8 rounded-sm text-xs" />
                      <Button type="submit" className="h-8 rounded-sm gap-1 !px-3"><PlusIcon /> Add</Button>
                    </form>

                    <div className="rounded-sm border border-zinc-200 dark:border-zinc-900 max-h-[120px] overflow-y-auto bg-zinc-50/20 dark:bg-zinc-950/20">
                      {(!activeProject.pendingTasks || activeProject.pendingTasks.length === 0) ? (
                        <div className="p-6 text-center text-[11px] text-zinc-500 italic">Pool is empty. Populate items above.</div>
                      ) : (
                        <ul className="divide-y divide-zinc-200/65 dark:divide-zinc-900/60">
                          {activeProject.pendingTasks.map((task) => (
                            <li key={task.id} className="flex items-center justify-between p-2 pl-2.5 group">
                              <span className="text-xs font-semibold tracking-tight truncate max-w-[200px]">{task.text}</span>
                              <div className="flex items-center gap-1.5 shrink-0">
                                <Button variant="outline" onClick={() => handleConvertTaskToCheckpoint(task)} className="text-[9px] font-extrabold uppercase tracking-wider px-2 h-6 gap-0.5 border-emerald-500/20 text-emerald-500 dark:text-emerald-400 dark:hover:bg-emerald-950/20">
                                  <ArrowUpRightIcon /> Convert
                                </Button>
                                <button onClick={() => handleDeleteQuickTask(task.id)} className="text-zinc-400 hover:text-red-500 p-0.5"><TrashIcon /></button>
                              </div>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  </div>
                </div>

              </div>
            </Card>

            {/* Interactive Timeline Display */}
            <Card className="p-8 md:p-12">
              <div className="mb-14 space-y-1.5">
                <h1 className="text-xl font-extrabold tracking-tight">{activeProject.title}</h1>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 max-w-xl leading-relaxed">{activeProject.description}</p>
              </div>

              <div className="w-full relative select-none">
                {(!activeProject.checkpoints || activeProject.checkpoints.length === 0) ? (
                  <div className="text-center py-10 border border-dashed border-zinc-200 dark:border-zinc-900 rounded-md">
                    <p className="text-zinc-500 text-[11px] font-semibold tracking-tight">Timeline is empty. Convert task pool items above to instantiate tracking circles.</p>
                  </div>
                ) : (
                  <div className="relative py-4 flex items-center justify-center">
                    <div className="absolute top-[28px] left-6 right-6 h-[2.5px] bg-zinc-200 dark:bg-zinc-800 z-0 hidden md:block" />
                    <div className="absolute left-1/2 top-[28px] bottom-16 w-[2.5px] -translate-x-1/2 bg-zinc-200 dark:bg-zinc-800 z-0 block md:hidden" />

                    <div className="relative z-10 w-full flex flex-col md:flex-row items-center justify-between md:justify-around gap-12 md:gap-4">
                      {activeProject.checkpoints.map((cp, index) => {
                        const completed = (cp.checklist || []).filter(t => t.isCompleted).length;
                        const progress = (cp.checklist || []).length > 0 ? Math.round((completed / cp.checklist.length) * 100) : 100;
                        const radius = 22;
                        const circumference = 2 * Math.PI * radius;
                        const strokeDashoffset = circumference - (progress / 100) * circumference;

                        return (
                          <div key={cp.id} onClick={() => setSelectedCheckpointId(cp.id)} className="relative group cursor-pointer flex flex-col items-center">
                            <div className="w-14 h-14 relative flex items-center justify-center rounded-full transition-transform duration-250 bg-white dark:bg-[#09090b]">
                              <svg className="absolute inset-0 w-full h-full transform -rotate-90">
                                <circle cx="28" cy="28" r={radius} fill="none" strokeWidth="2.5" className="stroke-zinc-150 dark:stroke-zinc-800" />
                                <circle cx="28" cy="28" r={radius} fill="none" strokeWidth="2.5" className="stroke-zinc-900 dark:stroke-zinc-100" strokeDasharray={circumference} strokeDashoffset={strokeDashoffset} strokeLinecap="round" />
                              </svg>
                              <div className={`w-10 h-10 rounded-full flex items-center justify-center shadow-2xs transition-all ${isDarkMode ? 'bg-zinc-100 text-zinc-950 group-hover:bg-white' : 'bg-zinc-900 text-zinc-50 group-hover:bg-zinc-950'}`}>
                                {renderCheckpointIcon(cp.icon, index)}
                              </div>
                            </div>

                            <div className="mt-3 text-center flex flex-col items-center">
                              <span className="text-[11px] font-bold tracking-tight max-w-[130px] truncate block">{cp.title}</span>
                              {cp.deadline ? (
                                <span className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-1 font-semibold flex items-center gap-1 select-none">
                                  <CalendarIcon /> {formatDate(cp.deadline)}
                                </span>
                              ) : cp.subtitle ? (
                                <span className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-0.5 font-medium">{cp.subtitle}</span>
                              ) : null}
                            </div>

                            <button onClick={(e) => handleRemoveCheckpoint(cp.id, e)} className="absolute -top-1 -right-1 opacity-0 group-hover:opacity-100 transition-opacity bg-red-500 text-white rounded-full p-1 hover:bg-red-600"><XIcon /></button>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            </Card>
          </main>

          {/* Configuration Detail Modal */}
          {activeCheckpoint && (
            <div className="fixed inset-0 bg-black/60 dark:bg-black/85 backdrop-blur-xs z-50 flex items-center justify-center p-4 overflow-y-auto">
              <div className="relative w-full max-w-lg rounded-lg border border-zinc-200 bg-white text-zinc-900 shadow-xl overflow-hidden transition-all duration-250 animate-in fade-in zoom-in-95 dark:border-zinc-900 dark:bg-[#09090b] dark:text-zinc-100">
                <div className="flex items-center justify-between p-4.5 border-b border-zinc-150 dark:border-zinc-900 bg-zinc-50/50 dark:bg-zinc-950/40">
                  <div className="flex items-center gap-2">
                    <Badge>Checkpoint Setup</Badge>
                    <span className="text-[10px] text-zinc-400 font-bold tracking-tight flex items-center gap-1"><EditIcon /> Local Save</span>
                  </div>
                  <button onClick={() => setSelectedCheckpointId(null)} className="text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 p-1"><XIcon /></button>
                </div>

                <div className="p-6 space-y-5 max-h-[65vh] overflow-y-auto scrollbar-thin">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-1.5">
                      <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-500">Checkpoint Title</label>
                      <Input type="text" value={activeCheckpoint.title || ''} onChange={e => handleUpdateCheckpointDetail(activeCheckpoint.id, 'title', e.target.value)} className="h-8 text-xs font-semibold" />
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-500">Timeframe Subtitle</label>
                      <Input type="text" value={activeCheckpoint.subtitle || ''} onChange={e => handleUpdateCheckpointDetail(activeCheckpoint.id, 'subtitle', e.target.value)} placeholder="e.g. ~2 weeks" className="h-8 text-xs" />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 pt-1">
                    <div className="space-y-1.5">
                      <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-500">Deadline Target</label>
                      <div className="relative">
                        <Input type="date" value={activeCheckpoint.deadline || ''} onChange={e => handleUpdateCheckpointDetail(activeCheckpoint.id, 'deadline', e.target.value)} className="h-8 rounded-sm text-xs font-semibold pl-8 dark:color-scheme-dark transition-all focus:border-zinc-400" />
                        <CalendarIcon className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-zinc-400 pointer-events-none" />
                      </div>
                    </div>
                    <div className="space-y-1.5">
                      <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-500">Active Marker</label>
                      <Badge className="h-8 w-full justify-center text-xs font-semibold py-0 rounded-sm">
                        {activeCheckpoint.icon ? activeCheckpoint.icon.toUpperCase() : 'DEFAULT'}
                      </Badge>
                    </div>
                  </div>

                  {/* Icon Selector Grid */}
                  <div className="space-y-1.5 pt-1">
                    <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-500">Select Marker Icon</label>
                    <div className="grid grid-cols-5 gap-1.5">
                      {AVAILABLE_ICONS.map((iconItem) => {
                        const isSelected = activeCheckpoint.icon === iconItem.name || (!activeCheckpoint.icon && iconItem.name === 'number');
                        return (
                          <button
                            key={iconItem.name}
                            type="button"
                            onClick={() => handleUpdateCheckpointDetail(activeCheckpoint.id, 'icon', iconItem.name)}
                            className={`h-8 flex items-center justify-center rounded border text-xs font-semibold transition-all ${
                              isSelected 
                                ? "bg-zinc-900 border-zinc-900 text-zinc-50 dark:bg-zinc-100 dark:border-zinc-100 dark:text-zinc-950" 
                                : "border-zinc-200 hover:bg-zinc-50 dark:border-zinc-800 dark:hover:bg-zinc-900 text-zinc-400 dark:text-zinc-500"
                            }`}
                          >
                            {iconItem.icon ? React.createElement(iconItem.icon, { className: "w-3.5 h-3.5" }) : iconItem.label}
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-550">Headline Summary</label>
                    <Input type="text" value={activeCheckpoint.headline || ''} onChange={e => handleUpdateCheckpointDetail(activeCheckpoint.id, 'headline', e.target.value)} placeholder="Focus statement of milestone" className="h-8 text-xs" />
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-550">Description Details</label>
                    <Textarea value={activeCheckpoint.description || ''} onChange={e => handleUpdateCheckpointDetail(activeCheckpoint.id, 'description', e.target.value)} placeholder="Objectives layout description..." className="min-h-[60px] resize-none text-xs leading-relaxed" />
                  </div>

                  {/* Deliverables checklist */}
                  <div className="space-y-3 pt-4 border-t border-zinc-200 dark:border-zinc-900">
                    <span className="text-[9px] font-bold tracking-wider uppercase text-zinc-400 block">Checkpoint Checklist</span>
                    <form onSubmit={(e) => handleAddModalChecklistItem(activeCheckpoint.id, e)} className="flex gap-1.5">
                      <Input type="text" value={modalNewTaskText} onChange={e => setModalNewTaskText(e.target.value)} placeholder="Add deliverable focus target..." className="h-8 text-xs" />
                      <Button type="submit" className="h-8 shrink-0 !px-3">Add</Button>
                    </form>

                    {(!activeCheckpoint.checklist || activeCheckpoint.checklist.length === 0) ? (
                      <p className="text-[11px] italic text-zinc-500 py-1">No tasks defined for milestone yet.</p>
                    ) : (
                      <div className="space-y-1">
                        {activeCheckpoint.checklist.map((task) => (
                          <div key={task.id} className="flex items-center justify-between p-2.5 rounded-sm border transition-all bg-white dark:bg-zinc-950 border-zinc-200 dark:border-zinc-900">
                            <label className="flex items-center gap-2.5 cursor-pointer select-none flex-1 min-w-0">
                              <input type="checkbox" className="sr-only" checked={task.isCompleted} onChange={() => handleToggleTask(activeCheckpoint.id, task.id)} />
                              <div className={`w-3.5 h-3.5 rounded border flex items-center justify-center shrink-0 ${task.isCompleted ? 'bg-zinc-900 border-zinc-900 text-zinc-50 dark:bg-zinc-100 dark:text-zinc-950 dark:border-zinc-100' : 'border-zinc-300 bg-white dark:border-zinc-800 dark:bg-zinc-900'}`}>
                                {task.isCompleted && <CheckIcon />}
                              </div>
                              <span className={`text-xs font-semibold truncate ${task.isCompleted ? 'line-through text-zinc-400 dark:text-zinc-550 font-medium' : ''}`}>{task.text}</span>
                            </label>
                            <button onClick={() => handleRemoveModalChecklistItem(activeCheckpoint.id, task.id)} className="text-zinc-400 hover:text-red-500 p-0.5"><TrashIcon /></button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                <div className="flex items-center justify-end p-4 border-t border-zinc-150 dark:border-zinc-900 bg-zinc-50/20 dark:bg-zinc-950/20">
                  <Button variant="outline" onClick={() => setSelectedCheckpointId(null)} className="h-8">Close details</Button>
                </div>
              </div>
            </div>
          )}
        </div>
      );
    }

    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
  </script>
</body>
</html>
"""

# Render the macOS high-fidelity workspace inside the Streamlit view
components.html(html_app, height=1080, scrolling=True)
