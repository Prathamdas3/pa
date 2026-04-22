import { createFileRoute } from "@tanstack/react-router";
import {
  AlertCircle,
  Calendar,
  CheckCircle2,
  Clock,
  Pencil,
  Plus,
  Tag,
  Trash2,
  X,
  Check,
  Loader2,
} from "lucide-react";
import { useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  useCreateTask,
  useDeleteTask,
  useGetTasks,
  useUpdateTask,
  type Task,
  type TaskCreate,
  type TaskUpdate,
} from "#/hooks/task";

export const Route = createFileRoute("/tasks")({
  component: TasksPage,
});

// ─────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────

type Priority = "low" | "medium" | "high";
type Status = "pending" | "in_progress" | "completed";

// ─────────────────────────────────────────────
// Helpers
// ─────────────────────────────────────────────

function getStatusIcon(status: Status) {
  switch (status) {
    case "completed":
      return <CheckCircle2 className="h-4 w-4 text-emerald-500" />;
    case "in_progress":
      return <Clock className="h-4 w-4 text-blue-500" />;
    default:
      return <AlertCircle className="h-4 w-4 text-amber-500" />;
  }
}

function getPriorityVariant(priority: Priority): "destructive" | "secondary" | "outline" {
  switch (priority) {
    case "high": return "destructive";
    case "medium": return "secondary";
    default: return "outline";
  }
}

// ─────────────────────────────────────────────
// Create Form
// ─────────────────────────────────────────────

function CreateTaskForm() {
  const createTask = useCreateTask();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<Priority>("medium");
  const [status, setStatus] = useState<Status>("pending");
  const [dueDate, setDueDate] = useState("");
  const [tagInput, setTagInput] = useState("");
  const [tags, setTags] = useState<string[]>([]);

  const addTag = () => {
    const trimmed = tagInput.trim();
    if (trimmed && !tags.includes(trimmed)) {
      setTags((prev) => [...prev, trimmed]);
    }
    setTagInput("");
  };

  const removeTag = (tag: string) => setTags((prev) => prev.filter((t) => t !== tag));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    const payload: TaskCreate = {
      title: title.trim(),
      description: description.trim() || undefined,
      priority,
      status,
      due_date: dueDate || undefined,
      tags: tags.length > 0 ? tags : undefined,
    };

    await createTask.mutateAsync(payload);

    // Reset form
    setTitle("");
    setDescription("");
    setPriority("medium");
    setStatus("pending");
    setDueDate("");
    setTags([]);
    setTagInput("");
  };

  return (
    <Card className="sticky top-24 border-primary/20 shadow-sm transition-all hover:border-primary/40">
      <CardHeader>
        <CardTitle className="text-xl">Create New Task</CardTitle>
        <CardDescription>Define a new task to track your progress</CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {/* Title */}
          <div className="space-y-1.5">
            <label className="text-sm font-medium">Title *</label>
            <Input
              placeholder="Review BTC daily candle..."
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>

          {/* Description */}
          <div className="space-y-1.5">
            <label className="text-sm font-medium">Description</label>
            <Input
              placeholder="Optional details..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          {/* Priority + Status */}
          <div className="grid grid-cols-2 gap-3">
            <div className="space-y-1.5">
              <label className="text-sm font-medium">Priority</label>
              <Select value={priority} onValueChange={(v) => setPriority(v as Priority)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">Low</SelectItem>
                  <SelectItem value="medium">Medium</SelectItem>
                  <SelectItem value="high">High</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-1.5">
              <label className="text-sm font-medium">Status</label>
              <Select value={status} onValueChange={(v) => setStatus(v as Status)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="pending">Pending</SelectItem>
                  <SelectItem value="in_progress">In Progress</SelectItem>
                  <SelectItem value="completed">Completed</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Due Date */}
          <div className="space-y-1.5">
            <label className="text-sm font-medium">Due Date</label>
            <Input
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
            />
          </div>

          {/* Tags */}
          <div className="space-y-1.5">
            <label className="text-sm font-medium">Tags</label>
            <div className="flex gap-2">
              <Input
                placeholder="Add a tag..."
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    addTag();
                  }
                }}
              />
              <Button type="button" variant="outline" size="sm" onClick={addTag}>
                <Plus className="h-4 w-4" />
              </Button>
            </div>
            {tags.length > 0 && (
              <div className="flex flex-wrap gap-1.5 pt-1">
                {tags.map((tag) => (
                  <span
                    key={tag}
                    className="flex items-center gap-1 rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium"
                  >
                    {tag}
                    <button
                      type="button"
                      onClick={() => removeTag(tag)}
                      className="ml-0.5 text-muted-foreground hover:text-foreground"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>
        </CardContent>

        <CardFooter>
          <Button type="submit" className="w-full" disabled={createTask.isPending}>
            {createTask.isPending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Adding...
              </>
            ) : (
              <>
                Add Task
                <Plus className="ml-2 h-4 w-4" />
              </>
            )}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}

// ─────────────────────────────────────────────
// Editable Task Card
// ─────────────────────────────────────────────

function TaskCard({ task }: { task: Task }) {
  const deleteTask = useDeleteTask();
  const updateTask = useUpdateTask(task.id);

  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description ?? "");
  const [editPriority, setEditPriority] = useState<Priority>(task.priority);
  const [editStatus, setEditStatus] = useState<Status>(task.status);
  const [editDueDate, setEditDueDate] = useState(task.due_date ?? "");
  const [editTagInput, setEditTagInput] = useState("");
  const [editTags, setEditTags] = useState<string[]>(task.tags ?? []);

  const addTag = () => {
    const trimmed = editTagInput.trim();
    if (trimmed && !editTags.includes(trimmed)) {
      setEditTags((prev) => [...prev, trimmed]);
    }
    setEditTagInput("");
  };

  const removeTag = (tag: string) =>
    setEditTags((prev) => prev.filter((t) => t !== tag));

  const handleSave = async () => {
    const payload: TaskUpdate = {
      title: editTitle.trim(),
      description: editDescription.trim() || undefined,
      priority: editPriority,
      status: editStatus,
      due_date: editDueDate || undefined,
      tags: editTags.length > 0 ? editTags : undefined,
    };
    await updateTask.mutateAsync(payload);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditTitle(task.title);
    setEditDescription(task.description ?? "");
    setEditPriority(task.priority);
    setEditStatus(task.status);
    setEditDueDate(task.due_date ?? "");
    setEditTags(task.tags ?? []);
    setIsEditing(false);
  };

  return (
    <Card className="group relative overflow-hidden transition-all hover:bg-muted/30">
      <div className="p-6">
        {isEditing ? (
          /* ── Edit Mode ── */
          <div className="space-y-4">
            <Input
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="font-bold"
              placeholder="Task title"
            />
            <Input
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              placeholder="Description"
            />

            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1">
                <label className="text-xs font-medium text-muted-foreground uppercase">Priority</label>
                <Select value={editPriority} onValueChange={(v) => setEditPriority(v as Priority)}>
                  <SelectTrigger className="h-8 text-sm">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">Low</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="high">High</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-1">
                <label className="text-xs font-medium text-muted-foreground uppercase">Status</label>
                <Select value={editStatus} onValueChange={(v) => setEditStatus(v as Status)}>
                  <SelectTrigger className="h-8 text-sm">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="pending">Pending</SelectItem>
                    <SelectItem value="in_progress">In Progress</SelectItem>
                    <SelectItem value="completed">Completed</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-xs font-medium text-muted-foreground uppercase">Due Date</label>
              <Input
                type="date"
                value={editDueDate}
                onChange={(e) => setEditDueDate(e.target.value)}
                className="h-8 text-sm"
              />
            </div>

            <div className="space-y-1">
              <label className="text-xs font-medium text-muted-foreground uppercase">Tags</label>
              <div className="flex gap-2">
                <Input
                  placeholder="Add tag..."
                  value={editTagInput}
                  className="h-8 text-sm"
                  onChange={(e) => setEditTagInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      addTag();
                    }
                  }}
                />
                <Button type="button" variant="outline" size="sm" onClick={addTag}>
                  <Plus className="h-3.5 w-3.5" />
                </Button>
              </div>
              {editTags.length > 0 && (
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {editTags.map((tag) => (
                    <span
                      key={tag}
                      className="flex items-center gap-1 rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium"
                    >
                      {tag}
                      <button type="button" onClick={() => removeTag(tag)}>
                        <X className="h-3 w-3 text-muted-foreground hover:text-foreground" />
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>

            <div className="flex gap-2 pt-1">
              <Button
                size="sm"
                onClick={handleSave}
                disabled={updateTask.isPending}
                className="flex-1"
              >
                {updateTask.isPending ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <>
                    <Check className="mr-1.5 h-3.5 w-3.5" />
                    Save
                  </>
                )}
              </Button>
              <Button size="sm" variant="outline" onClick={handleCancel} className="flex-1">
                <X className="mr-1.5 h-3.5 w-3.5" />
                Cancel
              </Button>
            </div>
          </div>
        ) : (
          /* ── View Mode ── */
          <>
            <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  {getStatusIcon(task.status)}
                  <h3 className="font-bold uppercase tracking-wide">{task.title}</h3>
                </div>
                <p className="text-sm text-muted-foreground">
                  {task.description || "No description provided."}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant={getPriorityVariant(task.priority)} className="capitalize">
                  {task.priority}
                </Badge>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100 hover:text-primary"
                  onClick={() => setIsEditing(true)}
                >
                  <Pencil className="h-4 w-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100 hover:text-destructive"
                  onClick={() => deleteTask.mutate(task.id)}
                  disabled={deleteTask.isPending}
                >
                  {deleteTask.isPending ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Trash2 className="h-4 w-4" />
                  )}
                </Button>
              </div>
            </div>

            <Separator className="my-4" />

            <div className="flex flex-wrap items-center gap-4 text-[10px] font-bold uppercase text-muted-foreground">
              <div className="flex items-center gap-1.5">
                <Calendar className="h-3 w-3" />
                <span>Created {new Date(task.created_at).toLocaleDateString()}</span>
              </div>
              {task.due_date && (
                <div className="flex items-center gap-1.5">
                  <Clock className="h-3 w-3" />
                  <span>Due {new Date(task.due_date).toLocaleDateString()}</span>
                </div>
              )}
              {task.tags && task.tags.length > 0 && (
                <div className="flex items-center gap-1.5">
                  <Tag className="h-3 w-3" />
                  <div className="flex gap-1">
                    {task.tags.map((tag) => (
                      <span key={tag} className="rounded bg-muted px-1.5 py-0.5">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </Card>
  );
}

// ─────────────────────────────────────────────
// Page
// ─────────────────────────────────────────────

function TasksPage() {
  const { data: tasks, isLoading, error } = useGetTasks();

  if (isLoading)
    return (
      <div className="flex h-64 items-center justify-center gap-2 text-muted-foreground">
        <Loader2 className="h-5 w-5 animate-spin" />
        <span>Loading your tasks...</span>
      </div>
    );

  if (error)
    return (
      <div className="p-8 text-center text-destructive">
        Error loading tasks: {(error as Error).message}
      </div>
    );

  return (
    <div className="container mx-auto max-w-5xl space-y-8 p-6 lg:p-10">
      <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight">Tasks</h1>
          <p className="text-muted-foreground">
            Manage and track your active trading tasks
          </p>
        </div>
        <Badge variant="outline" className="w-fit px-3 py-1 text-sm">
          {tasks?.length || 0} Total Tasks
        </Badge>
      </header>

      <div className="grid gap-8 lg:grid-cols-3">
        {/* Sidebar: Create Form */}
        <aside className="lg:col-span-1">
          <CreateTaskForm />
        </aside>

        {/* Main: Task List */}
        <div className="space-y-4 lg:col-span-2">
          {!tasks || tasks.length === 0 ? (
            <div className="flex h-48 flex-col items-center justify-center rounded-xl border border-dashed text-muted-foreground shadow-sm">
              <ClipboardList className="mb-2 h-10 w-10 opacity-20" />
              <p>No tasks found. Create one to get started!</p>
            </div>
          ) : (
            tasks.map((task) => <TaskCard key={task.id} task={task} />)
          )}
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// Icon
// ─────────────────────────────────────────────

function ClipboardList(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <title>Clipboard List Icon</title>
      <rect width="8" height="4" x="8" y="2" rx="1" ry="1" />
      <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
      <path d="M12 11h4" />
      <path d="M12 16h4" />
      <path d="M8 11h.01" />
      <path d="M8 16h.01" />
    </svg>
  );
}