import React, { useState, useEffect } from 'react';
import { 
  Plus, Check, Trash2, Sun, Moon, X, Folder, FolderPlus, ArrowUpRight, Edit3,
  Flag, Star, Rocket, Code, Palette, Search, Sparkles, Trophy, Target, Calendar
} from 'lucide-react';
import { initializeApp } from 'firebase/app';
import { getAuth, signInWithCustomToken, signInAnonymously, onAuthStateChanged } from 'firebase/auth';
import { getFirestore, doc, collection, onSnapshot, addDoc, updateDoc, deleteDoc } from 'firebase/firestore';

// ==========================================
// Firebase Initialization
// ==========================================
const firebaseConfig = typeof __firebase_config !== 'undefined' 
  ? JSON.parse(__firebase_config) 
  : { apiKey: "", authDomain: "", projectId: "", storageBucket: "", messagingSenderId: "", appId: "" };

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';

// ==========================================
// Icon System Config
// ==========================================
const AVAILABLE_ICONS = [
  { name: 'number', label: '#' },
  { name: 'flag', icon: Flag },
  { name: 'star', icon: Star },
  { name: 'rocket', icon: Rocket },
  { name: 'code', icon: Code },
  { name: 'palette', icon: Palette },
  { name: 'search', icon: Search },
  { name: 'sparkles', icon: Sparkles },
  { name: 'trophy', icon: Trophy },
  { name: 'target', icon: Target },
];

const renderCheckpointIcon = (iconName, index, className = "w-4 h-4") => {
  const strokeWidth = 2.5;
  switch (iconName) {
    case 'flag': return <Flag className={className} strokeWidth={strokeWidth} />;
    case 'star': return <Star className={className} strokeWidth={strokeWidth} />;
    case 'rocket': return <Rocket className={className} strokeWidth={strokeWidth} />;
    case 'code': return <Code className={className} strokeWidth={strokeWidth} />;
    case 'palette': return <Palette className={className} strokeWidth={strokeWidth} />;
    case 'search': return <Search className={className} strokeWidth={strokeWidth} />;
    case 'sparkles': return <Sparkles className={className} strokeWidth={strokeWidth} />;
    case 'trophy': return <Trophy className={className} strokeWidth={strokeWidth} />;
    case 'target': return <Target className={className} strokeWidth={strokeWidth} />;
    default: return <span className="font-bold font-mono text-xs">{index + 1}</span>;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return '';
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

// ==========================================
// Shadcn UI Component Abstractions
// ==========================================
const cn = (...classes) => classes.filter(Boolean).join(' ');

const Button = React.forwardRef(({ className, variant = 'default', size = 'default', ...props }, ref) => {
  const baseStyles = 'inline-flex items-center justify-center rounded-md text-xs font-semibold tracking-tight transition-all duration-200 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-zinc-400 disabled:pointer-events-none disabled:opacity-50 select-none active:scale-[0.98]';
  const variants = {
    default: 'bg-zinc-900 text-zinc-50 shadow-xs hover:bg-zinc-800 dark:bg-zinc-100 dark:text-zinc-950 dark:hover:bg-zinc-200',
    destructive: 'bg-red-500 text-zinc-50 shadow-xs hover:bg-red-600 dark:bg-red-950 dark:text-zinc-50 dark:hover:bg-red-900',
    outline: 'border border-zinc-200 bg-white shadow-2xs hover:bg-zinc-50 hover:text-zinc-900 dark:border-zinc-800 dark:bg-zinc-950 dark:hover:bg-zinc-900 dark:hover:text-zinc-50',
    secondary: 'bg-zinc-100 text-zinc-900 shadow-2xs hover:bg-zinc-200/80 dark:bg-zinc-800 dark:text-zinc-50 dark:hover:bg-zinc-700',
    ghost: 'hover:bg-zinc-100 hover:text-zinc-900 dark:hover:bg-zinc-900 dark:hover:text-zinc-50',
  };
  const sizes = {
    default: 'h-9 px-4 py-2',
    sm: 'h-8 rounded-md px-3 text-[11px]',
    icon: 'h-9 w-9',
  };
  return <button className={cn(baseStyles, variants[variant], sizes[size], className)} ref={ref} {...props} />;
});

const Input = React.forwardRef(({ className, type, ...props }, ref) => {
  return (
    <input
      type={type}
      className={cn(
        'flex h-9 w-full rounded-md border border-zinc-200 bg-zinc-50/30 px-3 py-1 text-sm shadow-2xs transition-all placeholder:text-zinc-400 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-zinc-900/50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-zinc-800 dark:bg-zinc-950/20 dark:placeholder:text-zinc-600 dark:focus-visible:ring-zinc-400/50',
        className
      )}
      ref={ref}
      {...props}
    />
  );
});

const Textarea = React.forwardRef(({ className, ...props }, ref) => {
  return (
    <textarea
      className={cn(
        'flex min-h-[60px] w-full rounded-md border border-zinc-200 bg-zinc-50/30 px-3 py-2 text-sm shadow-2xs transition-all placeholder:text-zinc-400 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-zinc-900/50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-zinc-800 dark:bg-zinc-950/20 dark:placeholder:text-zinc-600 dark:focus-visible:ring-zinc-400/50',
        className
      )}
      ref={ref}
      {...props}
    />
  );
});

const Card = ({ className, ...props }) => (
  <div className={cn('rounded-xl border border-zinc-200 bg-white text-zinc-950 shadow-xs dark:border-zinc-800/60 dark:bg-zinc-950 dark:text-zinc-50 transition-all duration-350', className)} {...props} />
);

const Badge = ({ className, variant = 'default', ...props }) => {
  const baseStyles = 'inline-flex items-center rounded-full border px-2.5 py-0.5 text-[10px] font-bold tracking-wider uppercase transition-colors focus:outline-none select-none';
  const variants = {
    default: 'border-transparent bg-zinc-900 text-zinc-50 dark:bg-zinc-50 dark:text-zinc-900',
    secondary: 'border-transparent bg-zinc-150 text-zinc-900 dark:bg-zinc-900 dark:text-zinc-300',
    outline: 'text-zinc-950 dark:text-zinc-50 border-zinc-200 dark:border-zinc-800',
  };
  return <div className={cn(baseStyles, variants[variant], className)} {...props} />;
};

// ==========================================
// Main Core Application Block
// ==========================================
export default function App() {
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [user, setUser] = useState(null);
  const [projects, setProjects] = useState([]);
  const [activeProjectId, setActiveProjectId] = useState(null);
  const [selectedCheckpointId, setSelectedCheckpointId] = useState(null);
  
  const [quickTaskText, setQuickTaskText] = useState('');
  const [modalNewTaskText, setModalNewTaskText] = useState('');

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  useEffect(() => {
    const initAuth = async () => {
      try {
        if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
          await signInWithCustomToken(auth, __initial_auth_token);
        } else {
          await signInAnonymously(auth);
        }
      } catch (err) {
        console.error("Auth session sync error:", err);
      }
    };
    initAuth();
    const unsubscribe = onAuthStateChanged(auth, setUser);
    return () => unsubscribe();
  }, []);

  useEffect(() => {
    if (!user) return;

    const projectsCollectionRef = collection(db, 'artifacts', appId, 'users', user.uid, 'projects');
    const unsubscribe = onSnapshot(projectsCollectionRef, (snapshot) => {
      const projList = [];
      snapshot.forEach(doc => {
        projList.push({ id: doc.id, ...doc.data() });
      });
      
      if (projList.length === 0) {
        const defaultProj = {
          title: 'Guidance from industry leaders',
          description: 'A curated roadmap designed to take your venture from a raw concept to a successful market launch.',
          pendingTasks: [
            { id: 'pt-1', text: 'Brand Identity Strategy' },
            { id: 'pt-2', text: 'Beta Analytics Integration' }
          ],
          checkpoints: [
            {
              id: 'cp-1',
              title: 'Ideation',
              headline: 'Brainstorm and validate your concept',
              subtitle: '~2 weeks',
              description: 'Gather insights from market research, customer interviews, and competitor analysis to refine your product idea.',
              icon: 'search',
              deadline: '2026-05-30',
              checklist: [
                { id: 't-1', text: 'Market research & insights', isCompleted: true },
                { id: 't-2', text: 'Competitor analysis', isCompleted: false },
                { id: 't-3', text: 'Define value proposition', isCompleted: false },
              ]
            },
            {
              id: 'cp-2',
              title: 'Development',
              headline: 'Build your MVP',
              subtitle: '~6 weeks',
              description: 'Design, prototype, and develop the minimum viable product. Iterate quickly based on early feedback and testing.',
              icon: 'code',
              deadline: '2026-07-15',
              checklist: [
                { id: 't-4', text: 'Draft wireframes', isCompleted: true },
                { id: 't-5', text: 'Set up database schema', isCompleted: true },
                { id: 't-6', text: 'Develop core functionality', isCompleted: false },
              ]
            }
          ]
        };
        addDoc(projectsCollectionRef, defaultProj);
      } else {
        setProjects(projList);
        if (!activeProjectId || !projList.some(p => p.id === activeProjectId)) {
          setActiveProjectId(projList[0].id);
        }
      }
    });

    return () => unsubscribe();
  }, [user, activeProjectId]);

  // Safe Scope Setup (Prevents ReferenceError compiling exceptions)
  const activeProject = projects.find(p => p.id === activeProjectId) || projects[0] || {
    id: '',
    title: 'Loading Workspace...',
    description: '',
    pendingTasks: [],
    checkpoints: []
  };

  const activeCheckpoint = (activeProject.checkpoints || []).find(cp => cp.id === selectedCheckpointId);

  if (!user) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-zinc-950 text-zinc-100 font-sans">
        <div className="w-5 h-5 border-[1.5px] border-zinc-800 border-t-zinc-200 rounded-full animate-spin mb-3"></div>
        <span className="text-[9px] font-bold tracking-widest uppercase text-zinc-500">Syncing Workspace Engine</span>
      </div>
    );
  }

  const handleCreateProject = async () => {
    const newProj = {
      title: 'New Project Roadmap',
      description: 'Describe your new project goals here.',
      pendingTasks: [],
      checkpoints: []
    };
    try {
      const docRef = await addDoc(collection(db, 'artifacts', appId, 'users', user.uid, 'projects'), newProj);
      setActiveProjectId(docRef.id);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteProject = async (projectId, e) => {
    e.stopPropagation();
    if (projects.length <= 1) return;
    try {
      await deleteDoc(doc(db, 'artifacts', appId, 'users', user.uid, 'projects', projectId));
      const remaining = projects.filter(p => p.id !== projectId);
      setActiveProjectId(remaining[0].id);
    } catch (err) {
      console.error(err);
    }
  };

  const handleUpdateProjectMeta = async (field, value) => {
    if (!activeProject.id) return;
    try {
      await updateDoc(doc(db, 'artifacts', appId, 'users', user.uid, 'projects', activeProject.id), {
        [field]: value
      });
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddQuickTask = async (e) => {
    e.preventDefault();
    if (!quickTaskText.trim() || !activeProject.id) return;
    const newTask = { id: `pt-${Date.now()}`, text: quickTaskText.trim() };
    try {
      await updateDoc(doc(db, 'artifacts', appId, 'users', user.uid, 'projects', activeProject.id), {
        pendingTasks: [...(activeProject.pendingTasks || []), newTask]
      });
      setQuickTaskText('');
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteQuickTask = async (taskId) => {
    if (!activeProject.id) return;
    const updatedTasks = (activeProject.pendingTasks || []).filter(t => t.id !== taskId);
    try {
      await updateDoc(doc(db, 'artifacts', appId, 'users', user.uid, 'projects', activeProject.id), {
        pendingTasks: updatedTasks
      });
    } catch (err) {
      console.error(err);
    }
  };

  const handleConvertTaskToCheckpoint = async (task) => {
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
    try {
      await updateDoc(doc(db, 'artifacts', appId, 'users', user.uid, 'projects', activeProject.id), {
        pendingTasks: (activeProject.pendingTasks || []).filter(t => t.id !== task.id),
        checkpoints: [...(activeProject.checkpoints || []), newCheckpoint]
      });
    } catch (err) {
      console.error(err);
    }
  };

  const handleUpdateCheckpointDetail = async (checkpointId, field, value) => {
    if (!activeProject.id) return;
    const updatedCheckpoints = (activeProject.checkpoints || []).map(cp => 
      cp.id === checkpointId ? { ...cp, [field]: value } : cp
    );
    try {
      await updateDoc(doc(db, 'artifacts', appId, 'users', user.uid, 'projects', activeProject.id), {
        checkpoints: updatedCheckpoints
      });
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddModalChecklistItem = async (checkpointId, e) => {
    e.preventDefault();
    if (!modalNewTaskText.trim() || !activeProject.id) return;
    const newItem = { id: `t-${Date.now()}`, text: modalNewTaskText.trim(), isCompleted: false };
    const updatedCheckpoints = (activeProject.checkpoints || []).map(cp => {
      if (cp.id === checkpointId) {
        return { ...cp, checklist: [...(cp.checklist || []), newItem] };
      }
      return cp;
    });
    try {
      await updateDoc(doc(db, 'artifacts', appId, 'users', user.uid, 'projects', activeProject.id), {
        checkpoints: updatedCheckpoints
      });
      setModalNewTaskText('');
    } catch (err) {
      console.error(err);
    }
  };

  const handleToggleTask = async (checkpointId, taskId) => {
    if (!activeProject.id) return;
    const updatedCheckpoints = (activeProject.checkpoints || []).map(cp => {
      if (cp.id === checkpointId) {
        return {
          ...cp,
          checklist: (cp.checklist || []).map(t => t.id === taskId ? { ...t, isCompleted: !t.isCompleted } : t)
        };
      }
      return cp;
    });
    try {
      await updateDoc(doc(db, 'artifacts', appId, 'users', user.uid, 'projects', activeProject.id), {
        checkpoints: updatedCheckpoints
      });
    } catch (err) {
      console.error(err);
    }
  };

  const handleRemoveModalChecklistItem = async (checkpointId, taskId) => {
    if (!activeProject.id) return;
    const updatedCheckpoints = (activeProject.checkpoints || []).map(cp => {
      if (cp.id === checkpointId) {
        return { ...cp, checklist: (cp.checklist || []).filter(t => t.id !== taskId) };
      }
      return cp;
    });
    try {
      await updateDoc(doc(db, 'artifacts', appId, 'users', user.uid, 'projects', activeProject.id), {
        checkpoints: updatedCheckpoints
      });
    } catch (err) {
      console.error(err);
    }
  };

  const handleRemoveCheckpoint = async (checkpointId, e) => {
    e.stopPropagation();
    if (!activeProject.id) return;
    const updatedCheckpoints = (activeProject.checkpoints || []).filter(cp => cp.id !== checkpointId);
    try {
      await updateDoc(doc(db, 'artifacts', appId, 'users', user.uid, 'projects', activeProject.id), {
        checkpoints: updatedCheckpoints
      });
      if (selectedCheckpointId === checkpointId) {
        setSelectedCheckpointId(null);
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className={`min-h-screen transition-colors duration-300 ${isDarkMode ? 'bg-[#09090b] text-zinc-50' : 'bg-zinc-55 text-zinc-900'} font-sans pb-24 antialiased`}>
      
      {/* Navbar Header */}
      <header className={`border-b transition-colors duration-300 ${isDarkMode ? 'border-zinc-900 bg-[#09090b]/90' : 'border-zinc-200 bg-white/90'} sticky top-0 backdrop-blur-lg z-40 px-6 md:px-12 py-4`}>
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className={`w-7 h-7 rounded-md flex items-center justify-center font-bold text-xs tracking-tight shadow-xs ${
              isDarkMode ? 'bg-zinc-100 text-zinc-950' : 'bg-zinc-900 text-zinc-50'
            }`}>
              T
            </div>
            <span className="font-extrabold text-sm tracking-tight">Timeline Workspace</span>
          </div>
          <Button variant="outline" size="icon" onClick={() => setIsDarkMode(!isDarkMode)} className="w-8 h-8">
            {isDarkMode ? <Sun className="w-3.5 h-3.5" /> : <Moon className="w-3.5 h-3.5" />}
          </Button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 md:px-12 pt-10 space-y-8 animate-in fade-in duration-300">
        
        {/* Project Selector Index Card */}
        <Card className="p-6 border-zinc-200 dark:border-zinc-900">
          <div className="flex items-center justify-between mb-4 pb-2 border-b border-zinc-100 dark:border-zinc-900">
            <div className="flex items-center gap-2">
              <Folder className="w-3.5 h-3.5 text-zinc-400" />
              <h2 className="text-[10px] font-bold tracking-widest uppercase text-zinc-400">Project Index</h2>
            </div>
            <Button variant="outline" size="sm" onClick={handleCreateProject} className="gap-1.5 h-7 rounded-sm border-dashed text-[11px]">
              <FolderPlus className="w-3 h-3" /> Create New
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
                      <Trash2 className="w-3 h-3" />
                    </button>
                  )}
                </div>
              );
            })}
          </div>
        </Card>

        {/* Configurations workspace settings block */}
        <Card className="overflow-hidden border-zinc-200 dark:border-zinc-900">
          <div className="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-zinc-100 dark:divide-zinc-900">
            
            {/* Left side Metadata setup parameters */}
            <div className="p-6 space-y-5">
              <h2 className="text-[10px] font-bold tracking-widest uppercase text-zinc-400">Settings</h2>
              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-500 dark:text-zinc-400">Header / Brand text</label>
                  <Input type="text" value={activeProject.title || ''} onChange={e => handleUpdateProjectMeta('title', e.target.value)} className="h-8 rounded-sm text-xs font-semibold" />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-500 dark:text-zinc-400">Description Summary</label>
                  <Textarea value={activeProject.description || ''} onChange={e => handleUpdateProjectMeta('description', e.target.value)} className="min-h-[80px] resize-none rounded-sm text-xs leading-relaxed" />
                </div>
              </div>
            </div>

            {/* Right side Task pool container queue block */}
            <div className="p-6 flex flex-col justify-between space-y-5">
              <div className="space-y-4">
                <div>
                  <h2 className="text-[10px] font-bold tracking-widest uppercase text-zinc-400">Tasks Pool</h2>
                  <p className="text-[11px] text-zinc-500 mt-0.5">Add checklist phases, then convert them into checkpoints.</p>
                </div>
                
                <form onSubmit={handleAddQuickTask} className="flex gap-1.5">
                  <Input type="text" required value={quickTaskText} onChange={e => setQuickTaskText(e.target.value)} placeholder="e.g., Wireframe layout" className="h-8 rounded-sm text-xs" />
                  <Button type="submit" size="sm" className="h-8 rounded-sm gap-1"><Plus className="w-3 h-3" /> Add</Button>
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
                            <Button variant="outline" size="sm" onClick={() => handleConvertTaskToCheckpoint(task)} className="text-[9px] font-extrabold uppercase tracking-wider px-2 h-6 gap-0.5 border-emerald-500/20 text-emerald-500 dark:text-emerald-400 dark:hover:bg-emerald-950/20">
                              <ArrowUpRight className="w-2.5 h-2.5" /> Convert
                            </Button>
                            <button onClick={() => handleDeleteQuickTask(task.id)} className="text-zinc-400 hover:text-red-500 p-0.5"><Trash2 className="w-3 h-3" /></button>
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

        {/* Visual Timeline Panel Card */}
        <Card className="p-8 md:p-12 border-zinc-200 dark:border-zinc-900">
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
                
                {/* Horizontal Desktop Connector line vectors */}
                <div className={`hidden md:block absolute top-[28px] left-6 right-6 h-[2px] ${isDarkMode ? 'bg-zinc-800' : 'bg-zinc-200'} z-0`} />

                {/* Vertical Mobile Connector line vectors */}
                <div className={`block md:hidden absolute left-1/2 top-[28px] bottom-16 w-[2px] -translate-x-1/2 ${isDarkMode ? 'bg-zinc-800' : 'bg-zinc-200'} z-0`} />

                {/* Timeline Row Mapping Node matrix */}
                <div className="relative z-10 w-full flex flex-col md:flex-row items-center justify-between md:justify-around gap-12 md:gap-4">
                  {activeProject.checkpoints.map((cp, index) => {
                    const completed = (cp.checklist || []).filter(t => t.isCompleted).length;
                    const progress = (cp.checklist || []).length > 0 ? Math.round((completed / cp.checklist.length) * 100) : 100;
                    
                    const radius = 22;
                    const circumference = 2 * Math.PI * radius;
                    const strokeDashoffset = circumference - (progress / 100) * circumference;

                    return (
                      <div key={cp.id} onClick={() => setSelectedCheckpointId(cp.id)} className="relative group cursor-pointer flex flex-col items-center">
                        
                        {/* Vector Progress Stroke circle track elements */}
                        <div className="w-14 h-14 relative flex items-center justify-center rounded-full transition-transform duration-250 bg-white dark:bg-[#09090b]">
                          <svg className="absolute inset-0 w-full h-full transform -rotate-90">
                            <circle cx="28" cy="28" r={radius} fill="none" strokeWidth="2.5" className="stroke-zinc-150 dark:stroke-zinc-800" />
                            <circle cx="28" cy="28" r={radius} fill="none" strokeWidth="2.5" className="stroke-zinc-900 dark:stroke-zinc-100" strokeDasharray={circumference} strokeDashoffset={strokeDashoffset} strokeLinecap="round" />
                          </svg>
                          <div className={`w-10 h-10 rounded-full flex items-center justify-center shadow-2xs transition-all ${isDarkMode ? 'bg-zinc-100 text-zinc-950 group-hover:bg-white' : 'bg-zinc-900 text-zinc-50 group-hover:bg-zinc-950'}`}>
                            {renderCheckpointIcon(cp.icon, index, "w-4 h-4")}
                          </div>
                        </div>

                        {/* Description mapping strictly under nodes element frame */}
                        <div className="mt-3 text-center flex flex-col items-center">
                          <span className="text-[11px] font-bold tracking-tight max-w-[130px] truncate block">{cp.title}</span>
                          {cp.deadline ? (
                            <span className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-1 font-semibold flex items-center gap-1 select-none">
                              <Calendar className="w-3 h-3 text-zinc-400" /> {formatDate(cp.deadline)}
                            </span>
                          ) : cp.subtitle ? (
                            <span className="text-[10px] text-zinc-400 dark:text-zinc-500 mt-0.5 font-medium">{cp.subtitle}</span>
                          ) : null}
                        </div>

                        <button onClick={(e) => handleRemoveCheckpoint(cp.id, e)} className="absolute -top-1 -right-1 opacity-0 group-hover:opacity-100 transition-opacity bg-red-500 text-white rounded-full p-1 hover:bg-red-600"><X className="w-3 h-3" /></button>
                      </div>
                    );
                  })}
                </div>

              </div>
            )}
          </div>
        </Card>

      </main>

      {/* Pop-up Overlay Dialogue Modal Configuration Block */}
      {activeCheckpoint && (
        <div className="fixed inset-0 bg-black/60 dark:bg-black/85 backdrop-blur-xs z-50 flex items-center justify-center p-4 overflow-y-auto">
          <div className="relative w-full max-w-lg rounded-lg border border-zinc-200 bg-white text-zinc-900 shadow-xl overflow-hidden transition-all duration-250 animate-in fade-in zoom-in-95 dark:border-zinc-900 dark:bg-[#09090b] dark:text-zinc-100">
            
            <div className="flex items-center justify-between p-4.5 border-b border-zinc-150 dark:border-zinc-900 bg-zinc-50/50 dark:bg-zinc-950/40">
              <div className="flex items-center gap-2">
                <Badge variant="secondary">Checkpoint Setup</Badge>
                <span className="text-[10px] text-zinc-400 font-bold tracking-tight flex items-center gap-1"><Edit3 className="w-3 h-3" /> Real-time Save</span>
              </div>
              <button onClick={() => setSelectedCheckpointId(null)} className="text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100 p-1"><X className="w-4 h-4" /></button>
            </div>

            <div className="p-6 space-y-5 max-h-[65vh] overflow-y-auto scrollbar-thin">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-400">Checkpoint Title</label>
                  <Input type="text" value={activeCheckpoint.title || ''} onChange={e => handleUpdateCheckpointDetail(activeCheckpoint.id, 'title', e.target.value)} className="h-8 text-xs font-semibold" />
                </div>
                <div className="space-y-1.5">
                  <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-400">Timeframe Subtitle</label>
                  <Input type="text" value={activeCheckpoint.subtitle || ''} onChange={e => handleUpdateCheckpointDetail(activeCheckpoint.id, 'subtitle', e.target.value)} placeholder="e.g. ~2 weeks" className="h-8 text-xs" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 pt-1">
                <div className="space-y-1.5">
                  <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-400">Deadline Target</label>
                  <div className="relative">
                    <Input type="date" value={activeCheckpoint.deadline || ''} onChange={e => handleUpdateCheckpointDetail(activeCheckpoint.id, 'deadline', e.target.value)} className="h-8 rounded-sm text-xs font-semibold pl-8 dark:color-scheme-dark transition-all focus:border-zinc-400" />
                    <Calendar className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-zinc-400 pointer-events-none" />
                  </div>
                </div>
                <div className="space-y-1.5">
                  <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-400">Active Marker</label>
                  <Badge variant="outline" className="h-8 w-full justify-center text-xs font-semibold py-0 rounded-sm">
                    {activeCheckpoint.icon ? activeCheckpoint.icon.toUpperCase() : 'DEFAULT'}
                  </Badge>
                </div>
              </div>

              {/* Icon selector button node matrix wrapper grid */}
              <div className="space-y-1.5 pt-1">
                <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-400">Select Marker Icon</label>
                <div className="grid grid-cols-5 gap-1.5">
                  {AVAILABLE_ICONS.map((iconItem) => {
                    const isSelected = activeCheckpoint.icon === iconItem.name || (!activeCheckpoint.icon && iconItem.name === 'number');
                    return (
                      <button
                        key={iconItem.name}
                        type="button"
                        onClick={() => handleUpdateCheckpointDetail(activeCheckpoint.id, 'icon', iconItem.name)}
                        className={cn(
                          "h-8 flex items-center justify-center rounded border text-xs font-semibold transition-all",
                          isSelected 
                            ? "bg-zinc-900 border-zinc-900 text-zinc-50 dark:bg-zinc-100 dark:border-zinc-100 dark:text-zinc-950" 
                            : "border-zinc-200 hover:bg-zinc-50 dark:border-zinc-800 dark:hover:bg-zinc-900 text-zinc-400 dark:text-zinc-500"
                        )}
                      >
                        {iconItem.icon ? React.createElement(iconItem.icon, { className: "w-3.5 h-3.5" }) : iconItem.label}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-400">Headline Summary</label>
                <Input type="text" value={activeCheckpoint.headline || ''} onChange={e => handleUpdateCheckpointDetail(activeCheckpoint.id, 'headline', e.target.value)} placeholder="Focus statement of milestone" className="h-8 text-xs" />
              </div>

              <div className="space-y-1.5">
                <label className="text-[9px] font-bold tracking-wider uppercase text-zinc-400">Description Details</label>
                <Textarea value={activeCheckpoint.description || ''} onChange={e => handleUpdateCheckpointDetail(activeCheckpoint.id, 'description', e.target.value)} placeholder="Objectives layout description..." className="min-h-[60px] resize-none text-xs leading-relaxed" />
              </div>

              {/* Sub items deliverables checklist mapper */}
              <div className="space-y-3 pt-4 border-t border-zinc-200 dark:border-zinc-900">
                <span className="text-[9px] font-bold tracking-wider uppercase text-zinc-400 block">Checkpoint Checklist deliverables</span>
                <form onSubmit={(e) => handleAddModalChecklistItem(activeCheckpoint.id, e)} className="flex gap-1.5">
                  <Input type="text" value={modalNewTaskText} onChange={e => setModalNewTaskText(e.target.value)} placeholder="Add deliverable target focus..." className="h-8 text-xs" />
                  <Button type="submit" size="sm" className="h-8 shrink-0">Add</Button>
                </form>

                {(!activeCheckpoint.checklist || activeCheckpoint.checklist.length === 0) ? (
                  <p className="text-[11px] italic text-zinc-500 py-1">No tasks defined for milestone yet.</p>
                ) : (
                  <div className="space-y-1">
                    {activeCheckpoint.checklist.map((task) => (
                      <div key={task.id} className={`flex items-center justify-between p-2.5 rounded-sm border transition-all ${task.isCompleted ? 'bg-zinc-50 border-zinc-200 opacity-60 dark:bg-zinc-900/30 dark:border-zinc-950/60' : 'bg-white border-zinc-200 dark:bg-zinc-950/10 dark:border-zinc-900'}`}>
                        <label className="flex items-center gap-2.5 cursor-pointer select-none flex-1 min-w-0">
                          <input type="checkbox" className="sr-only" checked={task.isCompleted} onChange={() => handleToggleTask(activeCheckpoint.id, task.id)} />
                          <div className={`w-3.5 h-3.5 rounded border flex items-center justify-center shrink-0 ${task.isCompleted ? 'bg-zinc-900 border-zinc-900 text-zinc-50 dark:bg-zinc-100 dark:text-zinc-950 dark:border-zinc-100' : 'border-zinc-300 bg-white dark:border-zinc-800 dark:bg-zinc-900'}`}>
                            {task.isCompleted && <Check className="w-2.5 h-2.5 stroke-[3.5]" />}
                          </div>
                          <span className={`text-xs font-semibold truncate ${task.isCompleted ? 'line-through text-zinc-400 dark:text-zinc-500 font-medium' : ''}`}>{task.text}</span>
                        </label>
                        <button onClick={() => handleRemoveModalChecklistItem(activeCheckpoint.id, task.id)} className="text-zinc-400 hover:text-red-500 p-0.5"><Trash2 className="w-3.5 h-3.5" /></button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            <div className="flex items-center justify-end p-4 border-t border-zinc-150 dark:border-zinc-900 bg-zinc-50/20 dark:bg-zinc-950/20">
              <Button variant="outline" size="sm" onClick={() => setSelectedCheckpointId(null)} className="h-8">Close details</Button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}
