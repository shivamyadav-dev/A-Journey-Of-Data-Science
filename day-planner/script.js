(function() {
  'use strict';

  const STORAGE_KEY = 'focusPlannerData.v1';
  const IST_TZ = 'Asia/Kolkata';

  const defaultState = () => ({
    profile: {
      timezone: IST_TZ
    },
    preferences: {
      wakeTime: '06:30',
      sleepTime: '23:30',
      breakfast: '08:30',
      lunch: '13:00',
      dinner: '21:10',
      tuitionStart: '16:00',
      tuitionEnd: '20:30',
      typingMinutes: 30,
      communicationMinutes: 30,
      pomodoroWork: 25,
      pomodoroShortBreak: 5,
      pomodoroLongBreak: 15
    },
    roadmap: generateRoadmap(new Date()),
    daily: {},
    stats: {
      totalPoints: 0,
      totalFocusSessions: 0,
      streakDays: 0,
      lastActiveDate: null
    }
  });

  function generateRoadmap(startDate) {
    const start = normalizeDate(startDate);
    const weeks = [
      { title: 'Week 1: Python Setup + Basics', tasks: [
        'Set up Python, VS Code, Git',
        'Python syntax: variables, control flow',
        'Functions, modules, virtualenv',
        'Mini-project: CLI calculator'
      ]},
      { title: 'Week 2: Data Structures + NumPy', tasks: [
        'Lists, dicts, sets, tuples',
        'NumPy arrays, vectorization',
        'Mini-project: Array ops notebook'
      ]},
      { title: 'Week 3: Pandas Core', tasks: [
        'Pandas Series/DataFrame',
        'Indexing, filtering, groupby',
        'Mini-project: Sales EDA'
      ]},
      { title: 'Week 4: Statistics I', tasks: [
        'Descriptive stats, distributions',
        'Probability, sampling',
        'Mini-project: A/B test simulation'
      ]},
      { title: 'Week 5: Visualization', tasks: [
        'Matplotlib/Seaborn basics',
        'Plot selection & story',
        'Mini-project: IMDB EDA'
      ]},
      { title: 'Week 6: SQL Basics', tasks: [
        'Select, where, group by, joins',
        'Window functions intro',
        'Mini-project: SQL case studies'
      ]},
      { title: 'Week 7: SQL Advanced', tasks: [
        'CTEs, window funcs advanced',
        'Optimization & indexes',
        'Mini-project: Analytics SQL'
      ]},
      { title: 'Week 8: ML Intro', tasks: [
        'Train/test split, CV, metrics',
        'Linear/logistic regression',
        'Mini-project: Classification'
      ]},
      { title: 'Week 9: Trees + Ensembles', tasks: [
        'Decision trees, RF, XGBoost',
        'Feature engineering',
        'Mini-project: Kaggle starter'
      ]},
      { title: 'Week 10: Unsupervised', tasks: [
        'Clustering, PCA',
        'Anomaly detection',
        'Mini-project: Customer segments'
      ]},
      { title: 'Week 11: Time Series', tasks: [
        'ETS/ARIMA basics',
        'Feature-based TS',
        'Mini-project: Forecasting'
      ]},
      { title: 'Week 12: Project 1 (EDA + ML)', tasks: [
        'End-to-end project repo',
        'Clean code, README, visuals'
      ]},
      { title: 'Week 13: PyTorch/TensorFlow Intro', tasks: [
        'Tensors, basic models',
        'Training loops',
        'Mini-project: MNIST'
      ]},
      { title: 'Week 14: MLOps Basics', tasks: [
        'Experiment tracking',
        'Pipelines with sklearn',
        'Intro to deployment'
      ]},
      { title: 'Week 15: Data Engineering Basics', tasks: [
        'APIs, data ingestion',
        'Airflow/Prefect basics',
        'Mini-project: ETL pipeline'
      ]},
      { title: 'Week 16: Project 2 (ML + Deployment)', tasks: [
        'Simple API for model',
        'Docker basics',
        'Cloud free tier deploy'
      ]},
      { title: 'Week 17: Feature Stores + Monitoring', tasks: [
        'Data drift, model drift',
        'Logging/alerts'
      ]},
      { title: 'Week 18: NLP or CV (choose one)', tasks: [
        'Tokenization/Embeddings or CNNs',
        'Mini-project: Text/CV'
      ]},
      { title: 'Week 19: Systems for DS', tasks: [
        'ML system design basics',
        'Batch vs streaming'
      ]},
      { title: 'Week 20: SQL + Python Interview', tasks: [
        'Leet-style SQL practice',
        'Pandas/NumPy drills'
      ]},
      { title: 'Week 21: Case Studies', tasks: [
        'Product analytics',
        'Experiment design, metrics'
      ]},
      { title: 'Week 22: Resume + Portfolio', tasks: [
        'Polish 2 projects',
        'Write case study blog'
      ]},
      { title: 'Week 23: Mock Interviews', tasks: [
        'Behavioral + tech mocks',
        'Communication practice'
      ]},
      { title: 'Week 24: Capstone', tasks: [
        'End-to-end DS project',
        'Deploy + writeup'
      ]}
    ];
    return { startISO: toISODate(start), weeks };
  }

  function loadState() {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaultState();
    try {
      const parsed = JSON.parse(raw);
      if (!parsed.roadmap || !parsed.roadmap.weeks) parsed.roadmap = generateRoadmap(new Date());
      return parsed;
    } catch {
      return defaultState();
    }
  }

  function saveState() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }

  function normalizeDate(d) {
    const dd = new Date(d);
    dd.setHours(0,0,0,0);
    return dd;
  }

  function toISODate(d) {
    const nd = normalizeDate(d);
    return nd.toISOString().slice(0,10);
  }

  function parseHM(hm) {
    const [h, m] = hm.split(':').map(Number);
    return h * 60 + m;
  }

  function minutesToHM(mins) {
    const h = Math.floor(mins / 60);
    const m = mins % 60;
    return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}`;
  }

  function clamp(n, min, max) { return Math.max(min, Math.min(max, n)); }

  let state = loadState();

  // Elements
  const tabs = document.querySelectorAll('.tab');
  const panels = document.querySelectorAll('.tab-panel');
  const pointsDisplay = document.getElementById('pointsDisplay');
  const streakDisplay = document.getElementById('streakDisplay');
  const datePicker = document.getElementById('datePicker');
  const prevDayBtn = document.getElementById('prevDayBtn');
  const nextDayBtn = document.getElementById('nextDayBtn');
  const timelineEl = document.getElementById('timeline');
  const autoPlanBtn = document.getElementById('autoPlanBtn');
  const newTaskBtn = document.getElementById('newTaskBtn');
  const taskDialog = document.getElementById('taskDialog');
  const taskDialogTitle = document.getElementById('taskDialogTitle');
  const timerDialog = document.getElementById('timerDialog');

  const taskForm = document.getElementById('taskForm');
  const taskTitle = document.getElementById('taskTitle');
  const taskCategory = document.getElementById('taskCategory');
  const taskStart = document.getElementById('taskStart');
  const taskEnd = document.getElementById('taskEnd');
  const taskDuration = document.getElementById('taskDuration');
  const taskPoints = document.getElementById('taskPoints');
  const taskFixed = document.getElementById('taskFixed');
  const saveTaskBtn = document.getElementById('saveTaskBtn');

  const installBtn = document.getElementById('installBtn');
  const exportBtn = document.getElementById('exportBtn');
  const importInput = document.getElementById('importInput');

  const roadmapStartDate = document.getElementById('roadmapStartDate');
  const rebuildRoadmapBtn = document.getElementById('rebuildRoadmapBtn');
  const roadmapList = document.getElementById('roadmapList');

  const weekPoints = document.getElementById('weekPoints');
  const last7Bars = document.getElementById('last7Bars');
  const focusSessionsMetric = document.getElementById('focusSessionsMetric');

  const wakeTime = document.getElementById('wakeTime');
  const sleepTime = document.getElementById('sleepTime');
  const breakfastTime = document.getElementById('breakfastTime');
  const lunchTime = document.getElementById('lunchTime');
  const dinnerTime = document.getElementById('dinnerTime');
  const tuitionStart = document.getElementById('tuitionStart');
  const tuitionEnd = document.getElementById('tuitionEnd');
  const typingMinutes = document.getElementById('typingMinutes');
  const communicationMinutes = document.getElementById('communicationMinutes');

  const pomodoroWork = document.getElementById('pomodoroWork');
  const pomodoroShort = document.getElementById('pomodoroShort');
  const pomodoroLong = document.getElementById('pomodoroLong');

  const resetDataBtn = document.getElementById('resetDataBtn');
  const saveSettingsBtn = document.getElementById('saveSettingsBtn');

  // Tabs
  tabs.forEach(btn => btn.addEventListener('click', () => {
    tabs.forEach(b => b.classList.remove('active'));
    panels.forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(`tab-${btn.dataset.tab}`).classList.add('active');
    if (btn.dataset.tab === 'stats') renderStats();
    if (btn.dataset.tab === 'roadmap') renderRoadmap();
    if (btn.dataset.tab === 'settings') renderSettings();
  }));

  // Date controls
  const todayISO = toISODate(new Date());
  datePicker.value = todayISO;
  prevDayBtn.addEventListener('click', () => {
    const d = new Date(datePicker.value);
    d.setDate(d.getDate() - 1);
    datePicker.value = toISODate(d);
    renderDay();
  });
  nextDayBtn.addEventListener('click', () => {
    const d = new Date(datePicker.value);
    d.setDate(d.getDate() + 1);
    datePicker.value = toISODate(d);
    renderDay();
  });
  datePicker.addEventListener('change', renderDay);

  // Install prompt
  let deferredPrompt = null;
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    installBtn.style.display = 'inline-block';
  });
  installBtn.addEventListener('click', async () => {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    await deferredPrompt.userChoice;
    deferredPrompt = null;
    installBtn.style.display = 'none';
  });

  // Import/Export
  exportBtn.addEventListener('click', () => {
    const data = JSON.stringify(state, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `focus-planner-${toISODate(new Date())}.json`;
    a.click();
    URL.revokeObjectURL(url);
  });
  importInput.addEventListener('change', async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    try {
      const imported = JSON.parse(text);
      state = imported;
      saveState();
      renderAll();
      alert('Import successful');
    } catch (err) {
      alert('Invalid JSON file');
    }
  });

  // Task dialog
  let editTaskId = null;
  newTaskBtn.addEventListener('click', () => openTaskDialog());
  saveTaskBtn.addEventListener('click', (e) => {
    e.preventDefault();
    saveTaskFromDialog();
  });

  function openTaskDialog(task) {
    taskDialogTitle.textContent = task ? 'Edit Task' : 'Add Task';
    editTaskId = task?.id || null;
    taskTitle.value = task?.title || '';
    taskCategory.value = task?.category || 'Study';
    taskStart.value = task?.start || '';
    taskEnd.value = task?.end || '';
    taskDuration.value = task?.duration || '';
    taskPoints.value = task?.points || '';
    taskFixed.checked = !!task?.fixed;
    taskDialog.showModal();
  }

  function saveTaskFromDialog() {
    const dateKey = datePicker.value;
    const day = ensureDay(dateKey);
    const task = {
      id: editTaskId || `t_${Date.now()}`,
      title: (taskTitle.value || '').trim(),
      category: taskCategory.value,
      start: taskStart.value || null,
      end: taskEnd.value || null,
      duration: taskDuration.value ? Number(taskDuration.value) : null,
      points: taskPoints.value ? Number(taskPoints.value) : null,
      fixed: taskFixed.checked,
      status: 'todo'
    };
    if (!task.title) return;

    if (editTaskId) {
      const idx = day.tasks.findIndex(t => t.id === editTaskId);
      if (idx !== -1) day.tasks[idx] = { ...day.tasks[idx], ...task };
    } else {
      day.tasks.push(task);
    }
    saveState();
    taskDialog.close();
    renderDay();
  }

  function ensureDay(dateKey) {
    if (!state.daily[dateKey]) state.daily[dateKey] = { tasks: [], score: { points: 0, completed: 0, focusSessions: 0 }, notes: '' };
    return state.daily[dateKey];
  }

  function ensureStreak(dateKey) {
    const last = state.stats.lastActiveDate;
    if (!last) {
      state.stats.streakDays = 1;
    } else {
      const lastDate = new Date(last);
      const currDate = new Date(dateKey);
      const diff = (normalizeDate(currDate) - normalizeDate(lastDate)) / (1000*60*60*24);
      if (diff === 1) state.stats.streakDays += 1;
      else if (diff > 1) state.stats.streakDays = 1;
    }
    state.stats.lastActiveDate = dateKey;
  }

  function renderDay() {
    const dateKey = datePicker.value;
    const day = ensureDay(dateKey);

    // Sort tasks by time
    day.tasks.sort((a, b) => {
      const sa = a.start ? parseHM(a.start) : 9999;
      const sb = b.start ? parseHM(b.start) : 9999;
      return sa - sb;
    });

    timelineEl.innerHTML = '';
    for (const task of day.tasks) {
      const card = document.createElement('div');
      card.className = `task-card category-${task.category.replaceAll(' ', '\\ ')} ${task.status === 'done' ? 'done' : ''}`;
      const time = document.createElement('div');
      time.className = 'task-time';
      time.textContent = task.start && task.end ? `${task.start} - ${task.end}` : (task.duration ? `${task.duration} min` : '');
      const title = document.createElement('div');
      title.className = 'task-title';
      title.textContent = task.title;
      const meta = document.createElement('div');
      meta.className = 'task-meta';
      meta.textContent = `${task.category} • ${task.points ?? pointsForTask(task)} pts`;
      const actions = document.createElement('div');
      actions.className = 'task-actions';

      const startBtn = document.createElement('button');
      startBtn.className = 'btn small';
      startBtn.textContent = '▶ Focus';
      startBtn.addEventListener('click', () => openTimer(task));

      const doneBtn = document.createElement('button');
      doneBtn.className = 'btn small';
      doneBtn.textContent = '✓ Done';
      doneBtn.addEventListener('click', () => completeTask(task));

      const editBtn = document.createElement('button');
      editBtn.className = 'btn small';
      editBtn.textContent = '✎ Edit';
      editBtn.addEventListener('click', () => openTaskDialog(task));

      const delBtn = document.createElement('button');
      delBtn.className = 'btn small';
      delBtn.textContent = '🗑';
      delBtn.addEventListener('click', () => deleteTask(task.id));

      actions.append(startBtn, doneBtn, editBtn, delBtn);

      card.append(time, title, meta, actions);
      timelineEl.appendChild(card);
    }

    updateScorebar(dateKey);
  }

  function pointsForTask(task) {
    const base = task.duration ? Math.round(task.duration / 30) * 10 : 10;
    const focusBoost = (task.category === 'Deep Work' || task.category === 'Study') ? 1.5 : 1.0;
    return Math.round(base * focusBoost);
  }

  function completeTask(task) {
    if (task.status === 'done') return;
    const dateKey = datePicker.value;
    const day = ensureDay(dateKey);
    task.status = 'done';
    const pts = task.points ?? pointsForTask(task);
    day.score.points += pts;
    day.score.completed += 1;
    state.stats.totalPoints += pts;
    ensureStreak(dateKey);
    saveState();
    renderDay();
  }

  function deleteTask(taskId) {
    const dateKey = datePicker.value;
    const day = ensureDay(dateKey);
    day.tasks = day.tasks.filter(t => t.id !== taskId);
    saveState();
    renderDay();
  }

  function updateScorebar(dateKey) {
    const day = ensureDay(dateKey);
    pointsDisplay.textContent = `Points: ${day.score.points}`;
    streakDisplay.textContent = `Streak: ${state.stats.streakDays}🔥`;
  }

  autoPlanBtn.addEventListener('click', () => {
    autoPlanDay(new Date(datePicker.value));
    renderDay();
  });

  function autoPlanDay(date) {
    const iso = toISODate(date);
    const day = ensureDay(iso);
    day.tasks = []; // rebuild for the day

    const p = state.preferences;
    const blocks = [];

    // Helper to push block
    const push = (title, category, startHM, endHM, durationOverride, fixed=true) => {
      const duration = durationOverride ?? (parseHM(endHM) - parseHM(startHM));
      blocks.push({ title, category, start: startHM, end: endHM, duration, fixed });
    };

    // Morning routine - India context: cool mornings
    push('Wake + Hygiene + Water', 'Health', p.wakeTime, minutesToHM(parseHM(p.wakeTime)+30));
    push('Exercise (walk/yoga/HIIT)', 'Health', minutesToHM(parseHM(p.wakeTime)+30), minutesToHM(parseHM(p.wakeTime)+30+45));
    push('Mindfulness + Plan day', 'Personal', minutesToHM(parseHM(p.wakeTime)+30+45), minutesToHM(parseHM(p.wakeTime)+30+45+30));

    // Breakfast (fixed time)
    push('Breakfast', 'Meal', p.breakfast, minutesToHM(parseHM(p.breakfast)+30));

    // Deep work blocks before heat/noise
    push('Deep Work 1: Python/Stats', 'Deep Work', minutesToHM(parseHM(p.breakfast)+30), minutesToHM(parseHM(p.breakfast)+30+90));
    push('Short Break', 'Break', minutesToHM(parseHM(p.breakfast)+30+90), minutesToHM(parseHM(p.breakfast)+30+90+15));
    push('Deep Work 2: SQL/Projects', 'Deep Work', minutesToHM(parseHM(p.breakfast)+30+90+15), minutesToHM(parseHM(p.breakfast)+30+90+15+90));

    // Typing practice
    push('Typing Practice', 'Typing', minutesToHM(parseHM(p.breakfast)+30+90+15+90), minutesToHM(parseHM(p.breakfast)+30+90+15+90 + p.typingMinutes));

    // Lunch (fixed time) + power nap/walk
    push('Lunch', 'Meal', p.lunch, minutesToHM(parseHM(p.lunch)+45));
    push('Nap/Walk', 'Break', minutesToHM(parseHM(p.lunch)+45), minutesToHM(parseHM(p.lunch)+45+30));

    // Communication practice + review
    push('Communication Practice', 'Communication', minutesToHM(parseHM(p.lunch)+45+30), minutesToHM(parseHM(p.lunch)+45+30 + p.communicationMinutes));
    push('Light Review / Flashcards', 'Study', minutesToHM(parseHM(p.lunch)+45+30 + p.communicationMinutes), minutesToHM(parseHM(p.lunch)+45+30 + p.communicationMinutes + 30));

    // Commute + Tuition (fixed)
    push('Commute/Prep for Tuition', 'Commute', minutesToHM(parseHM(p.tuitionStart)-45), p.tuitionStart);
    push('Tuition', 'Tuition', p.tuitionStart, p.tuitionEnd);
    push('Return/Unwind', 'Commute', p.tuitionEnd, minutesToHM(parseHM(p.tuitionEnd)+40));

    // Dinner (fixed)
    push('Dinner', 'Meal', p.dinner, minutesToHM(parseHM(p.dinner)+30));

    // Evening review + plan + personal
    push('Active Recall Review', 'Study', minutesToHM(parseHM(p.dinner)+30), minutesToHM(parseHM(p.dinner)+30+30));
    push('Plan Tomorrow + Journal', 'Personal', minutesToHM(parseHM(p.dinner)+30+30), minutesToHM(parseHM(p.dinner)+30+30+20));
    push('Wind down / Reading', 'Personal', minutesToHM(parseHM(p.dinner)+30+30+20), state.preferences.sleepTime);

    // Map roadmap to deep work blocks
    const weekIndex = getRoadmapWeekIndex(new Date(iso));
    const week = state.roadmap.weeks[weekIndex] || state.roadmap.weeks[0];
    blocks.forEach(b => {
      if (b.category === 'Deep Work') {
        const topic = week?.title || 'Roadmap Focus';
        b.title = `${b.title} • ${topic}`;
      }
    });

    // Convert blocks to tasks
    const tasks = blocks.map(b => ({
      id: `t_${b.title}_${b.start}`.replace(/\s+/g,'_'),
      title: b.title,
      category: b.category,
      start: b.start,
      end: b.end,
      duration: parseHM(b.end) - parseHM(b.start),
      points: null,
      fixed: b.fixed,
      status: 'todo'
    }));

    day.tasks = tasks;
    day.score = day.score || { points: 0, completed: 0, focusSessions: 0 };
    saveState();
  }

  function getRoadmapWeekIndex(date) {
    const start = new Date(state.roadmap.startISO);
    const diffMs = normalizeDate(date) - normalizeDate(start);
    const weeks = Math.floor(diffMs / (1000*60*60*24*7));
    return clamp(weeks, 0, state.roadmap.weeks.length - 1);
  }

  function renderRoadmap() {
    roadmapStartDate.value = state.roadmap.startISO;
    roadmapList.innerHTML = '';
    state.roadmap.weeks.forEach((w, i) => {
      const card = document.createElement('div');
      card.className = 'week-card';
      const title = document.createElement('div');
      title.className = 'week-title';
      const isCurrent = i === getRoadmapWeekIndex(new Date());
      title.textContent = `${i+1}. ${w.title}${isCurrent ? ' (current)' : ''}`;
      const ul = document.createElement('div');
      ul.className = 'week-tasks';
      w.tasks.forEach((t, idx) => {
        const lbl = document.createElement('label');
        const cb = document.createElement('input');
        cb.type = 'checkbox';
        cb.checked = !!w.completed?.[idx];
        cb.addEventListener('change', () => {
          if (!w.completed) w.completed = {};
          w.completed[idx] = cb.checked;
          saveState();
        });
        const span = document.createElement('span');
        span.textContent = t;
        const badge = document.createElement('span');
        badge.className = 'score-item';
        badge.textContent = cb.checked ? '✓' : '•';
        lbl.append(cb, span, badge);
        ul.appendChild(lbl);
      });
      card.append(title, ul);
      roadmapList.appendChild(card);
    });
  }

  rebuildRoadmapBtn.addEventListener('click', () => {
    if (!roadmapStartDate.value) return;
    state.roadmap = generateRoadmap(new Date(roadmapStartDate.value));
    saveState();
    renderRoadmap();
  });

  // Settings
  function renderSettings() {
    const p = state.preferences;
    wakeTime.value = p.wakeTime;
    sleepTime.value = p.sleepTime;
    breakfastTime.value = p.breakfast;
    lunchTime.value = p.lunch;
    dinnerTime.value = p.dinner;
    tuitionStart.value = p.tuitionStart;
    tuitionEnd.value = p.tuitionEnd;
    typingMinutes.value = p.typingMinutes;
    communicationMinutes.value = p.communicationMinutes;
    pomodoroWork.value = p.pomodoroWork;
    pomodoroShort.value = p.pomodoroShortBreak;
    pomodoroLong.value = p.pomodoroLongBreak;
  }

  saveSettingsBtn.addEventListener('click', () => {
    const p = state.preferences;
    p.wakeTime = wakeTime.value || p.wakeTime;
    p.sleepTime = sleepTime.value || p.sleepTime;
    p.breakfast = breakfastTime.value || p.breakfast;
    p.lunch = lunchTime.value || p.lunch;
    p.dinner = dinnerTime.value || p.dinner;
    p.tuitionStart = tuitionStart.value || p.tuitionStart;
    p.tuitionEnd = tuitionEnd.value || p.tuitionEnd;
    p.typingMinutes = Number(typingMinutes.value) || p.typingMinutes;
    p.communicationMinutes = Number(communicationMinutes.value) || p.communicationMinutes;
    p.pomodoroWork = Number(pomodoroWork.value) || p.pomodoroWork;
    p.pomodoroShortBreak = Number(pomodoroShort.value) || p.pomodoroShortBreak;
    p.pomodoroLongBreak = Number(pomodoroLong.value) || p.pomodoroLongBreak;
    saveState();
    alert('Settings saved');
  });

  resetDataBtn.addEventListener('click', () => {
    if (!confirm('This will erase all your local data. Continue?')) return;
    state = defaultState();
    saveState();
    renderAll();
  });

  // Stats
  function renderStats() {
    const last7 = [];
    const today = new Date();
    for (let i = 6; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(today.getDate() - i);
      const key = toISODate(d);
      const pts = state.daily[key]?.score?.points || 0;
      last7.push(pts);
    }
    last7Bars.innerHTML = '';
    const max = Math.max(10, ...last7);
    last7.forEach(v => {
      const bar = document.createElement('div');
      const h = Math.round((v / max) * 70);
      bar.style.height = `${h}px`;
      last7Bars.appendChild(bar);
    });

    // Week points
    const startOfWeek = new Date();
    startOfWeek.setDate(startOfWeek.getDate() - ((startOfWeek.getDay()+6)%7)); // Monday as 0
    let sum = 0;
    for (let i = 0; i < 7; i++) {
      const d = new Date(startOfWeek);
      d.setDate(startOfWeek.getDate() + i);
      const key = toISODate(d);
      sum += state.daily[key]?.score?.points || 0;
    }
    weekPoints.textContent = `${sum} pts`;
    focusSessionsMetric.textContent = `${state.stats.totalFocusSessions || 0}`;
  }

  // Pomodoro timer
  let timer = null;
  let remaining = 0;
  let timerMode = 'work';
  const timerDisplay = document.getElementById('timerDisplay');
  const startTimerBtn = document.getElementById('startTimerBtn');
  const pauseTimerBtn = document.getElementById('pauseTimerBtn');
  const resetTimerBtn = document.getElementById('resetTimerBtn');

  document.querySelectorAll('.timer-mode .btn').forEach(btn => btn.addEventListener('click', () => setTimerMode(btn.dataset.mode)));

  function setTimerMode(mode) {
    timerMode = mode;
    const p = state.preferences;
    const mins = mode === 'work' ? p.pomodoroWork : (mode === 'short' ? p.pomodoroShortBreak : p.pomodoroLongBreak);
    remaining = mins * 60;
    renderTimer();
  }

  function openTimer(task) {
    document.getElementById('timerTaskTitle').textContent = task?.title || 'Focus Timer';
    setTimerMode('work');
    timerDialog.showModal();
  }

  function renderTimer() {
    const m = Math.floor(remaining / 60);
    const s = remaining % 60;
    timerDisplay.textContent = `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
  }

  function tick() {
    if (remaining <= 0) {
      clearInterval(timer);
      timer = null;
      if (timerMode === 'work') {
        // credit a focus session
        const key = datePicker.value;
        const day = ensureDay(key);
        day.score.focusSessions += 1;
        state.stats.totalFocusSessions += 1;
        saveState();
        renderStats();
        try { new AudioContext(); } catch {}
        alert('Session done! Take a short break.');
      }
      return;
    }
    remaining -= 1;
    renderTimer();
  }

  startTimerBtn.addEventListener('click', () => {
    if (timer) return;
    timer = setInterval(tick, 1000);
  });
  pauseTimerBtn.addEventListener('click', () => {
    clearInterval(timer);
    timer = null;
  });
  resetTimerBtn.addEventListener('click', () => {
    setTimerMode(timerMode);
  });

  // Initial render
  function renderAll() {
    renderDay();
    renderRoadmap();
    renderStats();
    renderSettings();
  }

  // Pre-populate today if empty
  if (!state.daily[todayISO] || (state.daily[todayISO].tasks || []).length === 0) {
    autoPlanDay(new Date());
  }

  renderAll();
})();