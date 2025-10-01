import React, { useState } from "react";
import { createPipeline } from "../api";
import { useNavigate } from "react-router-dom";


export default function PipelineForm() {
  const [name, setName] = useState("");
  const [sourceType, setSourceType] = useState("csv");
  const [sourceConfig, setSourceConfig] = useState(
    '{"path":"/data/example.csv"}'
  );
  const [targetType, setTargetType] = useState("bigquery");
  const [targetConfig, setTargetConfig] = useState("{}");
  const [schedule, setSchedule] = useState("");
  const nav = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const payload = {
        name,
        source_type: sourceType,
        source_config: JSON.parse(sourceConfig),
        transform_config: { steps: [] },
        target_type: targetType,
        target_config: JSON.parse(targetConfig),
        schedule_cron: schedule || null,
      };
      const res = await createPipeline(payload);
      alert("Created: " + res.id);
      nav("/");
    } catch (err) {
      alert("Error: " + err.message);
    }
  }

  return (
    <div className="p-6 max-w-2xl">
      <h2 className="text-2xl font-semibold mb-4">Create Pipeline</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm">Name</label>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="mt-1 w-full border rounded p-2"
          />
        </div>

        <div>
          <label className="block text-sm">Source Type</label>
          <select
            value={sourceType}
            onChange={(e) => setSourceType(e.target.value)}
            className="mt-1 w-full border rounded p-2"
          >
            <option value="csv">CSV</option>
            <option value="api">API</option>
            <option value="db">DB</option>
          </select>
        </div>

        <div>
          <label className="block text-sm">Source Config (JSON)</label>
          <textarea
            rows={4}
            value={sourceConfig}
            onChange={(e) => setSourceConfig(e.target.value)}
            className="mt-1 w-full border rounded p-2 font-mono text-sm"
          />
        </div>

        <div>
          <label className="block text-sm">Target Type</label>
          <select
            value={targetType}
            onChange={(e) => setTargetType(e.target.value)}
            className="mt-1 w-full border rounded p-2"
          >
            <option value="bigquery">BigQuery</option>
            <option value="snowflake">Snowflake</option>
            <option value="redshift">Redshift</option>
          </select>
        </div>

        <div>
          <label className="block text-sm">Target Config (JSON)</label>
          <textarea
            rows={4}
            value={targetConfig}
            onChange={(e) => setTargetConfig(e.target.value)}
            className="mt-1 w-full border rounded p-2 font-mono text-sm"
          />
        </div>

        <div>
          <label className="block text-sm">Schedule (cron, optional)</label>
          <input
            value={schedule}
            onChange={(e) => setSchedule(e.target.value)}
            className="mt-1 w-full border rounded p-2"
            placeholder="e.g. */5 * * * *"
          />
        </div>

        <div>
          <button
            type="submit"
            className="px-4 py-2 bg-green-600 text-white rounded"
          >
            Create
          </button>
        </div>
      </form>
    </div>
  );
}
