import { useEffect, useMemo, useState } from "react";
import {
  Background,
  Controls,
  Handle,
  MarkerType,
  Position,
  ReactFlow,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import "@fontsource/manrope/500.css";
import "@fontsource/manrope/600.css";
import "@fontsource/manrope/700.css";
import "@fontsource/inter/400.css";
import "@fontsource/inter/500.css";
import "@fontsource/inter/600.css";
import {
  IconAdjustmentsHorizontal,
  IconArrowLeft,
  IconArrowNarrowRight,
  IconArrowsExchange,
  IconBriefcase,
  IconBuildingBank,
  IconCalendarTime,
  IconChartBar,
  IconChevronDown,
  IconCpu,
  IconDeviceLaptop,
  IconExternalLink,
  IconFileAnalytics,
  IconFilter,
  IconHeartHandshake,
  IconHeartbeat,
  IconInfoCircle,
  IconListDetails,
  IconMap2,
  IconMessageCircle,
  IconMessages,
  IconReportAnalytics,
  IconRotate,
  IconSearch,
  IconSettings,
  IconShoppingCart,
  IconTargetArrow,
  IconTimeline,
  IconTrophy,
  IconUsers,
  IconWorld,
  IconWorldLongitude,
  IconX,
} from "@tabler/icons-react";
import {
  evidence,
  experience,
  impactSummary,
  insights,
  levers,
  marketCopy,
  outcomes,
  proofStats,
} from "./data.js";

const iconMap = {
  users: IconUsers,
  radar: IconTargetArrow,
  world: IconWorld,
  service: IconHeartHandshake,
  strategy: IconChartBar,
  digital: IconDeviceLaptop,
  revenue: IconReportAnalytics,
  operations: IconSettings,
  ai: IconCpu,
  health: IconHeartbeat,
  trophy: IconTrophy,
  reach: IconUsers,
  calendar: IconCalendarTime,
  messages: IconMessages,
  ledger: IconFileAnalytics,
  fintech: IconBuildingBank,
  ecommerce: IconShoppingCart,
  consumer: IconDeviceLaptop,
  education: IconBriefcase,
  healthcare: IconHeartbeat,
  public: IconWorldLongitude,
  growth: IconChartBar,
};

const organizationIcon = {
  Samsung: "consumer",
  Praava: "healthcare",
  "Laser Treat": "healthcare",
  HSREP: "public",
  EMU: "education",
  SureCash: "fintech",
  Ekhanei: "ecommerce",
  ACCA: "education",
  Asiatic: "strategy",
};

const organizationOrder = [
  "SureCash",
  "Ekhanei",
  "Samsung",
  "ACCA",
  "Asiatic",
  "Praava",
  "Laser Treat",
  "EMU",
  "HSREP",
];

const lensOptions = ["All lenses", "Growth", "Health Communication", "Health-Tech", "Population Health"];

const viewMeta = {
  system: { label: "System map", icon: IconMap2 },
  atlas: { label: "T-shaped atlas", icon: IconChartBar },
  career: { label: "Career journey", icon: IconTimeline },
  markets: { label: "Two markets", icon: IconWorldLongitude },
};

const headlineProofStats = [
  proofStats[0],
  proofStats[1],
  proofStats[2],
  { value: "10M reached", label: "national G2P delivery at population scale", icon: "reach" },
];

const heroByView = {
  system: {
    eyebrow: "INTERACTIVE SYSTEM MAP",
    title: "Trace the work from human insight to measurable outcome.",
    description: "Every result begins with understanding behavior, then connecting strategy, growth, operations and technology.",
    emphasis: "Growth is the core; health is the deliberate application.",
  },
  atlas: {
    eyebrow: "T-SHAPED IMPACT ATLAS",
    title: "One deep capability. Many places to apply it.",
    description: "Growth is the vertical. Customer insight, brand, operations, technology, and health are the connected breadth.",
  },
  career: {
    eyebrow: "INTERACTIVE IMPACT MAP",
    title: "Growth is the core. Health is the deliberate application.",
    description: "Follow the capability as it compounds, from listening to customers to building systems that improve human outcomes.",
  },
  markets: {
    eyebrow: "TWO MARKETS · ONE TRANSFERABLE CAPABILITY",
    title: "Proven at scale in one market. Building a new evidence base in another.",
    description: "Bangladesh carries the long operating record; the United States adds public-health education, credentialed practice, and emerging evidence.",
  },
};

const journeyLenses = ["All", "Growth", "Health", "Operations", "Tech", "Population"];

const careerChapters = [
  {
    id: "customer-insight", number: 1, year: 2010, label: "Customer\nInsight", note: "~80K conversations", capability: "Behavior",
    sector: "Customer service", lenses: ["Growth"], roles: ["grameenphone"], organization: null,
    headline: "Listening before building strategy", what: "Learned consumer behavior from the frontline across premium, roaming, retailer, and mass-market interactions.",
  },
  {
    id: "brand-digital", number: 2, year: 2012, label: "Brand +\nDigital", note: "Strategy foundation", capability: "Brand",
    sector: "Brand & digital", lenses: ["Growth", "Tech"], roles: ["grey", "mgh", "asiatic"], organization: "Asiatic",
    headline: "Brand thinking expanded into digital growth", what: "Connected consumer insight, integrated planning, production discipline, and a new digital revenue engine.",
  },
  {
    id: "fintech-commerce", number: 3, year: 2014, label: "Fintech +\nE-commerce", note: "Access + trust", capability: "Digital",
    sector: "Fintech · E-commerce", lenses: ["Growth", "Tech", "Population"], roles: ["surecash", "ekhanei"], organization: "SureCash",
    headline: "Growth systems moved from access to trust", what: "Applied segmentation, field activation, category operations, and digital communication across finance and commerce.",
  },
  {
    id: "samsung", number: 4, year: 2016, label: "Samsung\n#1 globally for growth", note: "Product + GTM", capability: "Digital",
    sector: "Consumer tech", lenses: ["Growth", "Tech", "Operations"], roles: ["samsung"], organization: "Samsung",
    headline: "Product planning translated into market leadership", what: "Integrated portfolio, pricing, positioning, e-commerce, and launch execution across flagship and mass-market smartphones.",
  },
  {
    id: "education", number: 5, year: 2017, label: "Education", note: "Ecosystem growth", capability: "GTM",
    sector: "Professional education", lenses: ["Growth", "Operations"], roles: ["acca"], organization: "ACCA",
    headline: "Commercial discipline applied to an education ecosystem", what: "Built an employer-and-member operating model around conversion, retention, partnership, and national thought leadership.",
  },
  {
    id: "praava", number: 6, year: 2019, label: "Praava\nPrimary healthcare", note: "Growth + access", capability: "P&L",
    sector: "Primary healthcare", lenses: ["Growth", "Health", "Operations", "Tech", "Population"], roles: ["praava"], organization: "Praava",
    headline: "Growth directed toward health access", what: "Combined consumer insight, product strategy, revenue ownership, service design, and data to build durable core-care growth.",
  },
  {
    id: "lasertreat", number: 7, year: 2021, label: "LaserTreat\nCOO, growth +\noperations", note: "+16% revenue", capability: "Operations",
    sector: "Specialized healthcare", lenses: ["Growth", "Health", "Operations", "Tech"], roles: ["lasertreat"], organization: "Laser Treat",
    headline: "Growth + operations, working as one system", what: "Integrated demand, service delivery, operating discipline, and digital systems across a multi-entity clinical group.",
  },
  {
    id: "mph", number: 8, year: 2022, label: "MPH +\nCHES®", note: "Evidence + practice", capability: "Health communication",
    sector: "Public health education", lenses: ["Health", "Population"], roles: ["emu-health", "brac-uihp"], organization: "EMU",
    headline: "Transferable growth skills sharpened through public health", what: "Added behavioral science, evaluation, health education, and applied mentoring to a long operating background.",
  },
  {
    id: "emu", number: 9, year: 2024, label: "EMU", note: "Health + community", capability: "Health communication",
    sector: "Education · population health", lenses: ["Health", "Operations", "Population"], roles: ["emu-housing"], organization: "EMU",
    headline: "Communication systems applied to student wellbeing", what: "Led resident engagement, staff development, crisis readiness, and community connection through a structured operating model.",
  },
  {
    id: "current-focus", number: 10, year: 2026, label: "Current focus\nHealth communication ·\nHealth-tech ·\nPopulation health", note: "Growth remains the core", capability: "AI systems",
    sector: "Public & population health", lenses: ["Growth", "Health", "Tech", "Population"], roles: ["hsrep"], organization: "HSREP",
    headline: "Growth remains the core capability", what: "The current direction connects health communication, health technology, population health, and accountable AI-enabled systems.",
  },
];

const atlasBreadth = [
  { id: "behavior", label: "Customer behavior", icon: "users" },
  { id: "brand", label: "Brand", icon: "strategy" },
  { id: "digital", label: "Digital", icon: "digital" },
  { id: "operations", label: "Operations", icon: "operations" },
  { id: "ai", label: "AI systems", icon: "ai" },
  { id: "health-comms", label: "Health communication", icon: "health" },
  { id: "population", label: "Population health", icon: "public" },
];

const atlasGrowthStages = [
  { id: "listen", number: 1, label: "Listen", sublabel: "Customer insight", icon: "service" },
  { id: "position", number: 2, label: "Position", sublabel: "Brand + strategy", icon: "radar" },
  { id: "activate", number: 3, label: "Activate", sublabel: "Digital + GTM", icon: "digital" },
  { id: "scale", number: 4, label: "Scale", sublabel: "Revenue + reach", icon: "revenue" },
  { id: "systemize", number: 5, label: "Systemize", sublabel: "Operations + AI", icon: "operations" },
];

const atlasSectors = [
  { id: "fintech", label: "Fintech", icon: "fintech", organization: "SureCash", x: 150, y: 205, side: "left", proof: "10M beneficiaries" },
  { id: "ecommerce", label: "E-commerce", icon: "ecommerce", organization: "Ekhanei", x: 105, y: 335, side: "left", proof: "#1 in 2.5 months" },
  { id: "consumer", label: "Consumer tech", icon: "consumer", organization: "Samsung", x: 185, y: 465, side: "left", proof: "#1 globally for growth" },
  { id: "education", label: "Education", icon: "education", organization: "ACCA", x: 305, y: 555, side: "left", proof: "100% of targets" },
  { id: "primary", label: "Primary healthcare", icon: "healthcare", organization: "Praava", x: 835, y: 245, side: "right", proof: "~57% B2C CAGR" },
  { id: "specialized", label: "Specialized healthcare", icon: "healthcare", organization: "Laser Treat", x: 835, y: 400, side: "right", proof: "+16% revenue" },
  { id: "public", label: "Public health", icon: "public", organization: "HSREP", x: 775, y: 555, side: "right", proof: "Independent platform" },
];

const atlasLensOrganizations = {
  "All evidence": organizationOrder,
  Growth: ["SureCash", "Ekhanei", "Samsung", "ACCA", "Praava", "Laser Treat"],
  Health: ["Praava", "Laser Treat", "EMU", "HSREP"],
  Operations: ["SureCash", "Samsung", "ACCA", "Praava", "Laser Treat", "EMU"],
  Technology: ["SureCash", "Samsung", "Praava", "Laser Treat"],
  Population: ["SureCash", "Praava", "EMU", "HSREP"],
};

function Icon({ name, size = 19, stroke = 1.75 }) {
  const Component = iconMap[name] || IconInfoCircle;
  return <Component aria-hidden="true" size={size} stroke={stroke} />;
}

function SystemNode({ data }) {
  const tone = data.tone || "blue";
  return (
    <div
      className={`system-node system-node--${data.group} tone-${tone} ${data.active ? "is-active" : ""} ${data.dimmed ? "is-dimmed" : ""}`}
      aria-label={`${data.label}. ${data.sublabel || ""}`}
    >
      <Handle type="target" position={Position.Left} className="node-handle" isConnectable={false} />
      <span className="system-node__icon"><Icon name={data.icon} size={20} /></span>
      <span className="system-node__copy">
        <strong>{data.label}</strong>
        <small>{data.sublabel}</small>
      </span>
      {data.metric && <span className="system-node__metric">{data.metric}</span>}
      <Handle type="source" position={Position.Right} className="node-handle" isConnectable={false} />
    </div>
  );
}

function AtlasNode({ data }) {
  return (
    <div
      className={`atlas-node atlas-node--${data.kind} tone-${data.tone || "teal"} ${data.active ? "is-active" : ""} ${data.compared ? "is-compared" : ""} ${data.dimmed ? "is-dimmed" : ""}`}
      aria-label={data.ariaLabel || `${data.label}. ${data.sublabel || ""}`}
    >
      <Handle id="top" type="target" position={Position.Top} className="atlas-handle" isConnectable={false} />
      <Handle id="left" type="target" position={Position.Left} className="atlas-handle" isConnectable={false} />
      <Handle id="source-left" type="source" position={Position.Left} className="atlas-handle" isConnectable={false} />
      {data.kind !== "proof" && <span className="atlas-node__orb"><Icon name={data.icon} size={data.kind === "growth" ? 25 : 22} stroke={1.8} /></span>}
      {data.kind === "growth" ? (
        <span className="atlas-node__growth-copy"><b>{data.number}</b><strong>{data.label}</strong><small>{data.sublabel}</small></span>
      ) : data.kind === "proof" ? (
        <span className="atlas-node__proof-copy">{data.label}</span>
      ) : (
        <span className="atlas-node__label">{data.label}</span>
      )}
      <Handle id="right" type="source" position={Position.Right} className="atlas-handle" isConnectable={false} />
      <Handle id="target-right" type="target" position={Position.Right} className="atlas-handle" isConnectable={false} />
      <Handle id="bottom" type="source" position={Position.Bottom} className="atlas-handle" isConnectable={false} />
    </div>
  );
}

const nodeTypes = { systemNode: SystemNode, atlasNode: AtlasNode };

function atlasEdge({ id, source, target, kind = "capability", active = false, compared = false, sourceHandle = "right", targetHandle = "left" }) {
  const color = kind === "growth" ? "#F4A24C" : kind === "application" ? "#F4A24C" : kind === "health" ? "#0FB3B3" : kind === "proof" ? "#4C8ED9" : "var(--edge-muted)";
  return {
    id,
    source,
    target,
    sourceHandle,
    targetHandle,
    type: kind === "growth" ? "straight" : "default",
    animated: active,
    focusable: false,
    zIndex: active || compared ? 5 : 1,
    markerEnd: kind === "application" && active ? { type: MarkerType.ArrowClosed, width: 11, height: 11, color } : undefined,
    style: {
      stroke: compared ? "#4C8ED9" : color,
      strokeWidth: kind === "growth" ? 2.7 : active || compared ? 2.2 : 1,
      opacity: kind === "growth" ? 0.95 : active || compared ? 0.92 : 0.25,
      strokeDasharray: kind === "growth" ? undefined : kind === "application" ? "4 5" : "3 6",
    },
  };
}

function buildAtlasGraph(selectedOrganization, compareOrganization, hoveredCapability, atlasLens) {
  const allowedOrganizations = new Set(atlasLensOrganizations[atlasLens] || organizationOrder);
  const nodes = [];
  const edges = [];

  atlasBreadth.forEach((item, index) => {
    nodes.push({
      id: `breadth-${item.id}`,
      type: "atlasNode",
      position: { x: 75 + index * 153, y: 12 },
      draggable: false,
      selectable: true,
      focusable: true,
      data: { ...item, kind: "breadth", tone: "teal", active: hoveredCapability === item.id, ariaLabel: `${item.label}, applied breadth capability` },
    });
    if (index > 0) edges.push(atlasEdge({ id: `breadth-line-${index}`, source: `breadth-${atlasBreadth[index - 1].id}`, target: `breadth-${item.id}`, kind: "health", active: hoveredCapability === item.id || hoveredCapability === atlasBreadth[index - 1].id }));
  });

  atlasGrowthStages.forEach((item, index) => {
    nodes.push({
      id: `growth-${item.id}`,
      type: "atlasNode",
      position: { x: 495, y: 145 + index * 92 },
      draggable: false,
      selectable: true,
      focusable: true,
      data: { ...item, kind: "growth", tone: "amber", active: true, ariaLabel: `Growth stage ${item.number}: ${item.label}, ${item.sublabel}` },
    });
    // engine spine drawn as a continuous CSS line behind the stack (see .atlas-spine); no per-step edges (they rendered as "!" stubs)
  });

  atlasSectors.forEach((item) => {
    const isAllowed = allowedOrganizations.has(item.organization);
    const active = item.organization === selectedOrganization;
    const compared = item.organization === compareOrganization;
    nodes.push({
      id: `sector-${item.id}`,
      type: "atlasNode",
      position: { x: item.x, y: item.y },
      draggable: false,
      selectable: true,
      focusable: true,
      data: { ...item, kind: "sector", tone: item.side === "right" ? "teal" : "blue", active, compared, dimmed: !isAllowed, ariaLabel: `${item.label}. Click to inspect ${item.organization} evidence; shift-click to compare.` },
    });

    const proofX = item.side === "left" ? Math.max(0, item.x - 145) : Math.min(1040, item.x + 145);
    nodes.push({
      id: `proof-${item.id}`,
      type: "atlasNode",
      position: { x: proofX, y: item.y + 22 },
      draggable: false,
      selectable: true,
      focusable: true,
      data: { label: item.proof, organization: item.organization, kind: "proof", tone: item.side === "right" ? "teal" : "blue", active, compared, dimmed: !isAllowed, ariaLabel: `${item.organization} evidence: ${item.proof}` },
    });

    edges.push(atlasEdge({
      id: `proof-line-${item.id}`,
      source: item.side === "left" ? `proof-${item.id}` : `sector-${item.id}`,
      target: item.side === "left" ? `sector-${item.id}` : `proof-${item.id}`,
      kind: item.side === "right" ? "health" : "proof",
      active,
      compared,
    }));
  });

  const capabilityConnections = [
    ["behavior", "fintech"], ["behavior", "ecommerce"],
    ["brand", "consumer"], ["brand", "education"],
    ["digital", "ecommerce"], ["digital", "consumer"],
    ["operations", "fintech"], ["operations", "specialized"],
    ["ai", "consumer"], ["ai", "primary"],
    ["health-comms", "primary"], ["health-comms", "specialized"],
    ["population", "primary"], ["population", "public"],
  ];
  capabilityConnections.forEach(([capability, sector]) => {
    const sectorItem = atlasSectors.find((item) => item.id === sector);
    const active = hoveredCapability === capability || sectorItem?.organization === selectedOrganization;
    const compared = sectorItem?.organization === compareOrganization;
    edges.push(atlasEdge({ id: `cap-${capability}-${sector}`, source: `breadth-${capability}`, target: `sector-${sector}`, kind: sectorItem?.side === "right" ? "health" : "capability", active, compared, sourceHandle: "bottom", targetHandle: "top" }));
  });

  const growthApplications = [
    ["listen", "fintech"], ["position", "ecommerce"], ["activate", "consumer"], ["scale", "education"],
    ["listen", "primary"], ["position", "primary"], ["scale", "primary"], ["systemize", "specialized"], ["activate", "public"],
  ];
  growthApplications.forEach(([stage, sector]) => {
    const sectorItem = atlasSectors.find((item) => item.id === sector);
    const active = sectorItem?.organization === selectedOrganization;
    const compared = sectorItem?.organization === compareOrganization;
    edges.push(atlasEdge({
      id: `application-${stage}-${sector}`,
      source: `growth-${stage}`,
      target: `sector-${sector}`,
      kind: "application",
      active,
      compared,
      sourceHandle: sectorItem?.side === "left" ? "source-left" : "right",
      targetHandle: sectorItem?.side === "left" ? "target-right" : "left",
    }));
  });

  return { nodes, edges };
}

function edgeKey(source, target) {
  return `${source}::${target}`;
}

const insightLeverMap = {
  "customer-conversations": ["brand-strategy", "digital-gtm"],
  "behavior-signals": ["brand-strategy", "ai-systems", "health-communication"],
  "market-context": ["brand-strategy", "revenue-growth"],
  "service-experience": ["operations", "ai-systems", "health-communication"],
};

function insightLeverPairs(item) {
  return item.insights.flatMap((insight) => {
    const matched = (insightLeverMap[insight] || []).filter((lever) => item.levers.includes(lever));
    const targets = matched.length ? matched : item.levers.slice(0, 1);
    return targets.map((lever) => [insight, lever]);
  });
}

function buildEdges(items, selectedItems) {
  const aggregate = new Map();
  const selectedPairs = new Set();

  selectedItems.forEach((item) => {
    insightLeverPairs(item).forEach(([insight, lever]) => selectedPairs.add(edgeKey(`insight-${insight}`, `lever-${lever}`)));
    item.levers.forEach((lever) => selectedPairs.add(edgeKey(`lever-${lever}`, `org-${item.organization}`)));
    item.outcomes.forEach((outcome) => selectedPairs.add(edgeKey(`org-${item.organization}`, `outcome-${outcome}`)));
  });

  const add = (source, target, phase) => {
    const key = edgeKey(source, target);
    const current = aggregate.get(key) || { source, target, phase, count: 0 };
    current.count += 1;
    aggregate.set(key, current);
  };

  items.forEach((item) => {
    insightLeverPairs(item).forEach(([insight, lever]) => add(`insight-${insight}`, `lever-${lever}`, "growth"));
    item.levers.forEach((lever) => add(`lever-${lever}`, `org-${item.organization}`, "application"));
    item.outcomes.forEach((outcome) => add(`org-${item.organization}`, `outcome-${outcome}`, outcome === "human-health" ? "health" : "outcome"));
  });

  return [...aggregate.values()].map((edge) => {
    const active = selectedPairs.has(edgeKey(edge.source, edge.target));
    const color = !active
      ? "var(--edge-muted)"
      : edge.phase === "health"
        ? "#0FB3B3"
        : edge.phase === "outcome"
          ? "#4C8ED9"
          : "#F4A24C";
    return {
      id: edgeKey(edge.source, edge.target),
      source: edge.source,
      target: edge.target,
      type: "default",
      animated: active,
      focusable: false,
      zIndex: active ? 5 : 1,
      style: {
        stroke: color,
        strokeWidth: active ? Math.min(7 + edge.count * 0.65, 14) : Math.min(0.7 + edge.count * 0.28, 2.4),
        opacity: active ? 0.92 : 0.32,
      },
    };
  });
}

function buildNodes(items, selectedOrganization, activeEvidenceId) {
  const selectedItems = items.filter((item) => item.organization === selectedOrganization);
  const activeItems = selectedItems.filter((item) => item.id === activeEvidenceId).slice(0, 1);
  const tracedItems = activeItems.length ? activeItems : selectedItems.slice(0, 1);
  const activeInsights = new Set(tracedItems.flatMap((item) => item.insights));
  const activeLevers = new Set(tracedItems.flatMap((item) => item.levers));
  const activeOutcomes = new Set(tracedItems.flatMap((item) => item.outcomes));
  const organizationNames = organizationOrder.filter((name) => items.some((item) => item.organization === name));
  const orgSpacing = Math.min(60, 425 / Math.max(organizationNames.length - 1, 1));

  const nodes = [];
  insights.forEach((item, index) => {
    nodes.push({
      id: `insight-${item.id}`,
      type: "systemNode",
      position: { x: 0, y: 30 + index * 112 },
      draggable: false,
      selectable: false,
      focusable: true,
      ariaLabel: item.label,
      data: {
        ...item,
        group: "insight",
        tone: "blue",
        active: activeInsights.has(item.id),
        dimmed: selectedItems.length > 0 && !activeInsights.has(item.id),
      },
    });
  });
  levers.forEach((item, index) => {
    nodes.push({
      id: `lever-${item.id}`,
      type: "systemNode",
      position: { x: 338, y: 4 + index * 76 },
      draggable: false,
      selectable: false,
      focusable: true,
      ariaLabel: item.label,
      data: {
        ...item,
        group: "lever",
        tone: item.id === "health-communication" ? "teal" : "amber",
        active: activeLevers.has(item.id),
        dimmed: selectedItems.length > 0 && !activeLevers.has(item.id),
      },
    });
  });
  organizationNames.forEach((name, index) => {
    const orgItems = items.filter((item) => item.organization === name);
    const first = orgItems[0];
    const isHealth = ["Praava", "Laser Treat", "HSREP", "EMU"].includes(name);
    nodes.push({
      id: `org-${name}`,
      type: "systemNode",
      position: { x: 706, y: 2 + index * orgSpacing },
      draggable: false,
      selectable: true,
      focusable: true,
      ariaLabel: `${first.organizationLabel}, ${first.tenure}, ${orgItems.length} evidence points`,
      data: {
        label: first.organizationLabel,
        sublabel: first.tenure,
        metric: `${orgItems.length} ${orgItems.length === 1 ? "result" : "results"}`,
        icon: organizationIcon[name],
        group: "organization",
        organization: name,
        tone: isHealth ? "teal" : "blue",
        active: name === selectedOrganization,
        dimmed: Boolean(selectedOrganization && name !== selectedOrganization),
      },
    });
  });
  outcomes.forEach((item, index) => {
    nodes.push({
      id: `outcome-${item.id}`,
      type: "systemNode",
      position: { x: 1082, y: 4 + index * 76 },
      draggable: false,
      selectable: false,
      focusable: true,
      ariaLabel: item.label,
      data: {
        ...item,
        group: "outcome",
        active: activeOutcomes.has(item.id),
        dimmed: selectedItems.length > 0 && !activeOutcomes.has(item.id),
      },
    });
  });
  return { nodes, selectedItems, tracedItems };
}

function ProofChip({ item }) {
  return (
    <div className="proof-chip" title={item.label}>
      <Icon name={item.icon} size={18} />
      <span>{item.value}</span>
    </div>
  );
}

function Segmented({ value, onChange }) {
  return (
    <div className="view-switcher" aria-label="Choose impact view">
      {Object.entries(viewMeta).map(([id, item]) => {
        const ViewIcon = item.icon;
        return (
          <button key={id} className={value === id ? "is-selected" : ""} onClick={() => onChange(id)} aria-pressed={value === id}>
            <ViewIcon size={16} stroke={1.8} aria-hidden="true" />
            <span>{item.label}</span>
          </button>
        );
      })}
    </div>
  );
}

function Filters({ market, setMarket, yearStart, setYearStart, lens, setLens }) {
  const [lensOpen, setLensOpen] = useState(false);
  return (
    <div className="filter-row">
      <div className="market-control" aria-label="Filter by market">
        <span className="filter-label">Market</span>
        {[["both", "Both"], ["bd", "Bangladesh"], ["us", "United States"]].map(([id, label]) => (
          <button key={id} onClick={() => setMarket(id)} aria-pressed={market === id} className={market === id ? "is-selected" : ""}>{label}</button>
        ))}
      </div>
      <label className="year-control">
        <span className="filter-label">Year range</span>
        <select value={yearStart} onChange={(event) => setYearStart(Number(event.target.value))}>
          <option value="2009">2009 to 2026</option>
          <option value="2015">2015 to 2026</option>
          <option value="2021">2021 to 2026</option>
        </select>
        <IconChevronDown size={16} aria-hidden="true" />
      </label>
      <div className="lens-control">
        <button className={lens !== "All lenses" ? "is-active" : ""} onClick={() => setLensOpen((open) => !open)} aria-expanded={lensOpen}>
          <IconFilter size={18} stroke={1.8} aria-hidden="true" />
          <span>{lens}</span>
          <IconChevronDown size={15} aria-hidden="true" />
        </button>
        {lensOpen && (
          <div className="lens-menu" role="menu">
            {lensOptions.map((item) => (
              <button key={item} role="menuitemradio" aria-checked={lens === item} className={lens === item ? "is-selected" : ""} onClick={() => { setLens(item); setLensOpen(false); }}>
                <span>{item}</span>{lens === item && <span aria-hidden="true">●</span>}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function MapInspector({ selectedCase, selectedItems, compareOrganization, setCompareOrganization, openLedger, cycleEvidence }) {
  if (!selectedCase) return null;
  const compareCase = compareOrganization ? evidence.find((item) => item.organization === compareOrganization) : null;
  const lensTags = [...new Set(selectedItems.map((item) => item.lens))].slice(0, 3);
  const breadcrumbInsight = insights.find((item) => item.id === selectedCase.insights[0]);
  const breadcrumbLever = levers.find((item) => item.id === selectedCase.levers[0]);
  const breadcrumbOutcome = outcomes.find((item) => item.id === selectedCase.outcomes.at(-1));

  return (
    <section className={`evidence-inspector ${compareCase ? "has-comparison" : ""}`} aria-live="polite">
      <div className="inspector-summary">
        <span className="eyebrow">SELECTED CASE · {selectedCase.organization.toUpperCase()}</span>
        <h2>{selectedCase.title}</h2>
        <div className="tag-row">{lensTags.map((tag) => <span key={tag}>{tag}</span>)}</div>
        <p>{selectedCase.summary}</p>
      </div>
      <div className="path-and-metrics">
        <div className="path-trace" aria-label="Selected capability path">
          <span>{breadcrumbInsight?.label}</span><IconArrowNarrowRight /><span>{breadcrumbLever?.label}</span><IconArrowNarrowRight /><span>{selectedCase.sector}</span><IconArrowNarrowRight /><span>{breadcrumbOutcome?.label}</span>
        </div>
        <div className="metric-strip">
          {selectedItems.slice(0, 5).map((item) => (
            <button key={item.id} onClick={() => cycleEvidence(item.id)} title={item.title}>
              <strong>{item.metric}</strong><small>{item.title}</small>
            </button>
          ))}
        </div>
      </div>
      <div className="inspector-actions">
        <button className="primary-action" onClick={openLedger}>View evidence <IconArrowNarrowRight /></button>
        <button className="secondary-action" onClick={() => setCompareOrganization(compareCase ? null : selectedCase.organization === "Laser Treat" ? "Praava" : "Laser Treat")}>
          <IconArrowsExchange size={17} /> {compareCase ? "Close comparison" : `Compare with ${selectedCase.organization === "Laser Treat" ? "Praava" : "Laser Treat"}`}
        </button>
      </div>
      {compareCase && (
        <div className="comparison-callout">
          <span>COMPARISON · {compareCase.organization.toUpperCase()}</span>
          <strong>{compareCase.metric}</strong>
          <p>{compareCase.title}</p>
        </div>
      )}
    </section>
  );
}

function SystemMap({ filteredEvidence, selectedOrganization, setSelectedOrganization, activeEvidenceId, setActiveEvidenceId, openLedger }) {
  const [compareOrganization, setCompareOrganization] = useState(null);
  const [mapFlow, setMapFlow] = useState(null);
  useEffect(() => {
    if (!mapFlow) return;
    const refit = () => mapFlow.fitView({ padding: 0.06, minZoom: 0.2, maxZoom: 1.0 });
    const t = setTimeout(refit, 60);
    window.addEventListener("resize", refit);
    return () => { clearTimeout(t); window.removeEventListener("resize", refit); };
  }, [mapFlow]);
  const { nodes, selectedItems, tracedItems } = useMemo(() => buildNodes(filteredEvidence, selectedOrganization, activeEvidenceId), [filteredEvidence, selectedOrganization, activeEvidenceId]);
  const edges = useMemo(() => buildEdges(filteredEvidence, tracedItems), [filteredEvidence, tracedItems]);
  const selectedCase = selectedItems.find((item) => item.id === activeEvidenceId) || selectedItems[0] || filteredEvidence[0];

  return (
    <>
      <section className="map-panel" aria-label="Interactive insight-to-outcome system map">
        <div className="map-helper"><IconInfoCircle size={16} /><span>Select an organization to isolate its path. Every node is keyboard focusable.</span></div>
        <div className="column-headings" aria-hidden="true">
          <span><b>01</b> Human insight</span>
          <span><b>02</b> Growth levers</span>
          <span><b>03</b> Where applied</span>
          <span><b>04</b> Outcomes</span>
        </div>
        <div className="flow-stage">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={nodeTypes}
            nodesDraggable={false}
            nodesConnectable={false}
            nodesFocusable={false}
            edgesFocusable={false}
            elementsSelectable
            zoomOnDoubleClick={false}
            zoomOnScroll={false}
            zoomOnPinch={false}
            panOnScroll={false}
            panOnDrag={false}
            preventScrolling={false}
            minZoom={0.2}
            maxZoom={1.2}
            fitView
            fitViewOptions={{ padding: 0.06, minZoom: 0.2, maxZoom: 1.0 }}
            onInit={setMapFlow}
            proOptions={{ hideAttribution: true }}
            onNodeClick={(_, node) => {
              if (node.data.group === "organization") setSelectedOrganization(node.data.organization);
            }}
          >
            <Background color="var(--rf-grid, #16304a)" gap={28} size={1} />
          </ReactFlow>
        </div>
      </section>
      <MapInspector
        selectedCase={selectedCase}
        selectedItems={selectedItems}
        compareOrganization={compareOrganization}
        setCompareOrganization={setCompareOrganization}
        openLedger={openLedger}
        cycleEvidence={setActiveEvidenceId}
      />
      <div className="map-footer">
        <div className="career-scrubber">
          <span>Career evolution · 2009-2026</span>
          <div className="scrubber-line" aria-hidden="true">
            {["Customer service", "Brand", "Fintech", "Consumer tech", "Education", "Healthcare", "Public health"].map((item, index) => <span key={item} className={index >= 5 ? "is-health" : index === 0 ? "is-growth" : ""}><i></i>{item}</span>)}
          </div>
        </div>
        <div className="legend">
          <span><i className="legend-line growth"></i>Growth path</span>
          <span><i className="legend-line health"></i>Health outcome</span>
          <span><i className="legend-line tech"></i>Operations + tech</span>
          <span><i className="legend-line background"></i>Background relationship</span>
        </div>
        <div className="footer-actions">
          <button onClick={() => setSelectedOrganization("Praava")}><IconRotate size={17} />Reset map</button>
          <button onClick={openLedger}><IconListDetails size={17} />Show all evidence</button>
        </div>
      </div>
    </>
  );
}

function AtlasInspector({ selectedOrganization, compareOrganization, onOpenEvidence, onClearCompare, onCompare }) {
  const selectedItems = evidence.filter((item) => item.organization === selectedOrganization);
  const selectedCase = selectedItems[0];
  const compareCase = evidence.find((item) => item.organization === compareOrganization);
  const titleByOrganization = {
    SureCash: "Access systems built at national scale",
    Ekhanei: "Trust converted into category growth",
    Samsung: "Product planning scaled into market leadership",
    ACCA: "An ecosystem built around conversion and retention",
    Praava: "Growth directed toward health access",
    "Laser Treat": "Growth + operations as one clinical system",
    EMU: "Health communication applied in a new market",
    HSREP: "Evidence translated for public understanding",
  };
  const outcomeByOrganization = {
    SureCash: "Population access + national delivery",
    Ekhanei: "Market leadership + transaction growth",
    Samsung: "Global launch leadership + product growth",
    ACCA: "Member conversion + retention",
    Praava: "Human outcome + service growth",
    "Laser Treat": "Clinical growth + operating discipline",
    EMU: "Behavior change + community connection",
    HSREP: "Public-health communication across two markets",
  };
  const lensTags = [...new Set(selectedItems.flatMap((item) => [item.lens, item.levers.includes("operations") ? "Operations" : null]).filter(Boolean))].slice(0, 4);

  return (
    <aside className="atlas-inspector" aria-live="polite">
      <span className="eyebrow">{selectedCase?.organizationLabel?.toUpperCase() || selectedOrganization.toUpperCase()}</span>
      <h2>{titleByOrganization[selectedOrganization] || selectedCase?.title}</h2>
      <span className="detail-label">LENSES</span>
      <p className="atlas-lens-copy">{lensTags.join(" · ")}</p>
      <span className="detail-label">OUTCOME</span>
      <p>{outcomeByOrganization[selectedOrganization] || selectedCase?.summary}</p>
      {compareCase && (
        <div className="atlas-compare">
          <button onClick={onClearCompare} aria-label="Close comparison"><IconX size={15} /></button>
          <span>COMPARE · {compareCase.organization.toUpperCase()}</span>
          <strong>{compareCase.metric}</strong>
          <p>{compareCase.title}</p>
        </div>
      )}
      <div className="atlas-inspector-actions">
        <button className="atlas-open-evidence" onClick={onOpenEvidence}>Open case evidence <IconArrowNarrowRight size={18} /></button>
        <button className="atlas-compare-action" onClick={onCompare}><IconArrowsExchange size={16} />{compareCase ? "Close comparison" : `Compare with ${selectedOrganization === "Praava" ? "Laser Treat" : "Praava"}`}</button>
      </div>
    </aside>
  );
}

function TShapedAtlas({ selectedOrganization, setSelectedOrganization, openLedger }) {
  const [atlasLens, setAtlasLens] = useState("All evidence");
  const [compareOrganization, setCompareOrganization] = useState(null);
  const [hoveredCapability, setHoveredCapability] = useState(null);
  const [pinnedCapability, setPinnedCapability] = useState(null);
  const [flowInstance, setFlowInstance] = useState(null);
  const activeCapability = hoveredCapability || pinnedCapability;
  const graph = useMemo(() => buildAtlasGraph(selectedOrganization, compareOrganization, activeCapability, atlasLens), [selectedOrganization, compareOrganization, activeCapability, atlasLens]);

  useEffect(() => {
    if (!atlasSectors.some((item) => item.organization === selectedOrganization)) setSelectedOrganization("Praava");
  }, [selectedOrganization, setSelectedOrganization]);

  useEffect(() => {
    if (!flowInstance) return;
    const refit = () => flowInstance.fitView({ padding: 0.07, minZoom: 0.2, maxZoom: 1.02 });
    const t = setTimeout(refit, 60);
    window.addEventListener("resize", refit);
    return () => { clearTimeout(t); window.removeEventListener("resize", refit); };
  }, [flowInstance, graph]);

  const changeLens = (item) => {
    setAtlasLens(item);
    const allowed = atlasLensOrganizations[item] || organizationOrder;
    if (!allowed.includes(selectedOrganization)) {
      const first = atlasSectors.find((sector) => allowed.includes(sector.organization));
      if (first) setSelectedOrganization(first.organization);
    }
  };

  const resetAtlas = () => {
    setAtlasLens("All evidence");
    setSelectedOrganization("Praava");
    setCompareOrganization(null);
    setPinnedCapability(null);
    flowInstance?.fitView({ padding: 0.04, maxZoom: 1.03 });
  };

  return (
    <section className="atlas-view">
      <div className="atlas-toolbar">
        <div className="atlas-filter-group" aria-label="Filter atlas evidence">
          {Object.keys(atlasLensOrganizations).map((item) => <button key={item} onClick={() => changeLens(item)} className={atlasLens === item ? "is-selected" : ""} aria-pressed={atlasLens === item}>{item}</button>)}
        </div>
        <div className="atlas-color-key" aria-label="Evidence lenses">
          <span><i className="key-dot growth"></i>Growth</span><span><i className="key-dot health"></i>Health</span><span><i className="key-dot operations"></i>Operations</span><span><i className="key-dot tech"></i>Technology</span><span><i className="key-dot population"></i>Population</span>
        </div>
      </div>
      <div className="atlas-layout">
        <div className="atlas-canvas" aria-label="Interactive T-shaped capability atlas">
          <div className="atlas-bracket-label" aria-hidden="true">APPLIED BREADTH</div>
          <ReactFlow
            nodes={graph.nodes}
            edges={graph.edges}
            nodeTypes={nodeTypes}
            nodesDraggable={false}
            nodesConnectable={false}
            nodesFocusable={false}
            edgesFocusable={false}
            elementsSelectable
            multiSelectionKeyCode={null}
            panOnScroll={false}
            panOnDrag={false}
            zoomOnScroll={false}
            zoomOnPinch={false}
            zoomOnDoubleClick={false}
            preventScrolling={false}
            minZoom={0.2}
            maxZoom={1.2}
            fitView
            fitViewOptions={{ padding: 0.07, minZoom: 0.2, maxZoom: 1.02 }}
            onInit={setFlowInstance}
            proOptions={{ hideAttribution: true }}
            onNodeMouseEnter={(_, node) => { if (node.data.kind === "breadth") setHoveredCapability(node.data.id); }}
            onNodeMouseLeave={() => setHoveredCapability(null)}
            onNodeClick={(event, node) => {
              if (node.data.kind === "breadth") {
                setPinnedCapability((current) => current === node.data.id ? null : node.data.id);
                return;
              }
              if (!node.data.organization) return;
              if (event.shiftKey) setCompareOrganization((current) => current === node.data.organization ? null : node.data.organization);
              else { setSelectedOrganization(node.data.organization); setCompareOrganization(null); }
            }}
          >
          </ReactFlow>
        </div>
        <div className="atlas-side">
          <AtlasInspector selectedOrganization={selectedOrganization} compareOrganization={compareOrganization} onOpenEvidence={openLedger} onClearCompare={() => setCompareOrganization(null)} onCompare={() => setCompareOrganization((current) => current ? null : selectedOrganization === "Praava" ? "Laser Treat" : "Praava")} />
          <button className="atlas-reset" onClick={resetAtlas}><IconRotate size={16} />Reset view</button>
        </div>
      </div>
      <div className="atlas-instructions">
        <span><IconTargetArrow size={17} />Hover: trace capability</span>
        <span><IconMessageCircle size={17} />Click: inspect evidence</span>
        <span><IconArrowsExchange size={17} />Shift-click: compare</span>
        <span className="atlas-line-key"><i></i>Capability connection</span>
        <span className="atlas-line-key is-growth"><i></i>Growth application path</span>
      </div>
    </section>
  );
}

function CareerJourney({ openLedger, view, setView }) {
  const [journeyLens, setJourneyLens] = useState("All");
  const [selectedId, setSelectedId] = useState("lasertreat");
  const [detailOpen, setDetailOpen] = useState(true);
  const selectedIndex = Math.max(0, careerChapters.findIndex((item) => item.id === selectedId));
  const selected = careerChapters[selectedIndex];
  const selectedRoles = experience.filter((item) => selected.roles.includes(item.id));
  const selectedEvidence = evidence.filter((item) => item.organization === selected.organization);
  const keyMetric = selectedEvidence[0]?.metric || selectedRoles[0]?.proof?.split(";")[0] || selected.note;
  const capabilityMatches = (chapter) => journeyLens === "All" || chapter.lenses.includes(journeyLens);
  const snapshot = [...selectedEvidence.map((item) => item.summary), ...selectedRoles.map((item) => item.proof)].filter(Boolean).slice(0, 3);
  const sectorsApplied = [
    ["samsung", "Consumer tech", "consumer"], ["fintech-commerce", "Fintech", "fintech"], ["fintech-commerce", "E-commerce", "ecommerce"],
    ["education", "Education", "education"], ["praava", "Healthcare", "healthcare"], ["current-focus", "Public & population health", "public"],
  ];

  const chooseLens = (item) => {
    setJourneyLens(item);
    if (item !== "All" && !selected.lenses.includes(item)) {
      const next = careerChapters.find((chapter) => chapter.lenses.includes(item));
      if (next) setSelectedId(next.id);
    }
    setDetailOpen(true);
  };

  const chooseChapter = (id) => { setSelectedId(id); setDetailOpen(true); };
  const nextResult = () => { setSelectedId(careerChapters[(selectedIndex + 1) % careerChapters.length].id); setDetailOpen(true); };

  return (
    <section className="career-journey-view">
      <div className="journey-topbar">
        <Segmented value={view} onChange={setView} />
        <div className="journey-filter-group" aria-label="Filter career journey by lens">
          {journeyLenses.map((item) => <button key={item} onClick={() => chooseLens(item)} className={journeyLens === item ? "is-selected" : ""} aria-pressed={journeyLens === item}>{item}</button>)}
        </div>
      </div>
      <div className={`journey-layout ${detailOpen ? "has-inspector" : ""}`}>
        <div className="journey-canvas">
          <div className="journey-helper"><IconInfoCircle size={16} /><span>Click a milestone to inspect the evidence and every role inside that chapter.</span></div>
          <div className="journey-capability-row" aria-label="Capabilities across the career journey">
            {careerChapters.map((chapter, index) => {
              const repeated = index > 0 && careerChapters[index - 1].capability === chapter.capability;
              return <span key={chapter.id} className={`${repeated ? "is-empty" : ""} ${!capabilityMatches(chapter) ? "is-dimmed" : ""}`}>{repeated ? "" : chapter.capability}</span>;
            })}
          </div>
          <div className="journey-track-wrap">
            <span className="journey-axis-label">GROWTH<br />SPINE<br /><small>(DEPTH)</small></span>
            <div className="journey-track" role="list" aria-label="Ten career chapters">
              {careerChapters.map((chapter) => (
                <button
                  key={chapter.id}
                  role="listitem"
                  className={`${selected.id === chapter.id ? "is-selected" : ""} ${chapter.number >= 7 ? "is-health" : ""} ${!capabilityMatches(chapter) ? "is-dimmed" : ""}`}
                  onClick={() => chooseChapter(chapter.id)}
                  aria-pressed={selected.id === chapter.id}
                >
                  <b>{chapter.number}</b><i></i><strong>{chapter.label}</strong><small>{chapter.note}</small>
                </button>
              ))}
            </div>
          </div>
          <div className="journey-years" aria-hidden="true">{[2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024, 2026].map((year) => <span key={year}>{year}</span>)}</div>
          <div className="journey-sector-row">
            <span className="journey-sector-label">SECTORS<br />APPLIED<br /><small>6 sectors · 2 countries</small></span>
            {sectorsApplied.map(([chapterId, label, icon]) => (
              <button key={`${chapterId}-${label}`} onClick={() => chooseChapter(chapterId)}><Icon name={icon} size={25} /><span>{label}</span></button>
            ))}
          </div>
        </div>
        {detailOpen && (
          <aside className="journey-inspector" aria-live="polite">
            <button className="journey-close" onClick={() => setDetailOpen(false)} aria-label="Close career detail"><IconX size={19} /></button>
            <span className="eyebrow">{selected.sector.toUpperCase()}</span>
            <h2>{selected.headline}</h2>
            <div className="journey-key-result">
              <div><span>KEY RESULT</span><strong>{keyMetric}</strong></div>
              <div><Icon name={selected.capability === "Operations" ? "operations" : selected.capability === "AI systems" ? "ai" : "growth"} size={30} /><span>{selected.capability}<br />capability</span></div>
            </div>
            <span className="detail-label">WHAT I DID</span>
            <p>{selected.what}</p>
            <span className="detail-label">EXPERIENCE IN THIS CHAPTER</span>
            <div className="chapter-role-stack">
              {selectedRoles.map((role) => <div key={role.id}><strong>{role.company}</strong><span>{role.role}</span><small>{role.tenure}</small></div>)}
            </div>
            <span className="detail-label">EVIDENCE SNAPSHOT</span>
            <ul>{snapshot.map((item, index) => <li key={`${selected.id}-${index}`}>{item}</li>)}</ul>
            <button className="journey-primary" onClick={openLedger}>View evidence <IconArrowNarrowRight size={19} /></button>
            <button className="journey-secondary" onClick={nextResult}>Next result <IconArrowNarrowRight size={19} /></button>
          </aside>
        )}
      </div>
      <div className="journey-legend">
        <span>LEGEND</span><span><i className="growth"></i>Growth spine (depth)</span><span><i className="health"></i>Health application</span><span><i className="breadth"></i>Capability (breadth)</span><span><i className="milestone"></i>Milestone (click to inspect)</span><p>T-shaped career: deep in growth, applied across health and systems.</p>
      </div>
    </section>
  );
}

function MarketCard({ marketKey, onOpen }) {
  const content = marketCopy[marketKey];
  return (
    <article className={`market-card market-card--${marketKey}`}>
      <span className="eyebrow">{content.eyebrow.toUpperCase()}</span>
      <h3>{content.title}</h3>
      <p>{content.subtitle}</p>
      <div className="market-facts">
        {content.facts.map(([metric, detail]) => <div key={metric}><strong>{metric}</strong><span>{detail}</span></div>)}
      </div>
      <button onClick={onOpen}>Explore this market <IconArrowNarrowRight size={18} /></button>
    </article>
  );
}

function TwoMarkets({ setMarket, setView, setSelectedOrganization }) {
  const openMarket = (id) => {
    setMarket(id);
    setSelectedOrganization(id === "us" ? "EMU" : "Praava");
    setView("system");
  };
  return (
    <section className="markets-view">
      <div className="view-intro markets-intro">
        <span className="eyebrow">TWO MARKETS · ONE TRANSFERABLE CAPABILITY</span>
        <h2>Growth is the bridge. Health is the deliberate application.</h2>
        <p>Bangladesh provides the long record of scale. The United States adds public-health education, credentialed practice and emerging evidence.</p>
      </div>
      <div className="markets-grid">
        <MarketCard marketKey="bd" onOpen={() => openMarket("bd")} />
        <div className="capability-bridge">
          <span className="bridge-label">THE BRIDGE</span>
          <div className="bridge-core"><IconChartBar size={28} /><strong>Transferable growth capability</strong></div>
          <div className="bridge-path">
            <span>Customer insight</span><IconArrowNarrowRight /><span>Strategy</span><IconArrowNarrowRight /><span>Operations</span><IconArrowNarrowRight /><span>Health application</span>
          </div>
          <p>The capability transfers across countries; the evidence takes a market-specific form.</p>
        </div>
        <MarketCard marketKey="us" onOpen={() => openMarket("us")} />
      </div>
      <aside className="hsrep-platform-card">
        <div className="hsrep-mark">Hs</div>
        <div><span className="eyebrow">INDEPENDENT PUBLIC-HEALTH PLATFORM</span><h3>HSREP</h3><p>Cross-market public-health communication: 57,274 gross platform-reported views and impressions · $0 ad spend · two countries.</p></div>
        <button onClick={() => { setMarket("both"); setSelectedOrganization("HSREP"); setView("system"); }}>Trace HSREP evidence <IconArrowNarrowRight /></button>
      </aside>
    </section>
  );
}

function EvidenceLedger({ onClose, onSelect }) {
  const [query, setQuery] = useState("");
  const [ledgerLens, setLedgerLens] = useState("All lenses");
  const results = evidence.filter((item) => {
    const matchesLens = ledgerLens === "All lenses" || item.lens === ledgerLens;
    const haystack = `${item.organization} ${item.title} ${item.metric} ${item.sector}`.toLowerCase();
    return matchesLens && haystack.includes(query.toLowerCase());
  });

  useEffect(() => {
    const onKey = (event) => { if (event.key === "Escape") onClose(); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  return (
    <div className="modal-backdrop" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}>
      <section className="ledger-modal" role="dialog" aria-modal="true" aria-labelledby="ledger-title">
        <header>
          <div><span className="eyebrow">PROOF, NOT PROMISES</span><h2 id="ledger-title">The complete evidence ledger.</h2><p>All 21 quantified results from the Impact page.</p></div>
          <button className="icon-button" onClick={onClose} aria-label="Close evidence ledger"><IconX size={21} /></button>
        </header>
        <div className="ledger-summary">
          {impactSummary.reach.map((item) => <div key={item.metric}><strong>{item.metric}</strong><span>{item.detail}</span></div>)}
          <div><strong>{impactSummary.press.metric}</strong><span>{impactSummary.press.detail}</span></div>
        </div>
        <div className="ledger-toolbar">
          <label><IconSearch size={18} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search evidence, organization or metric" /></label>
          <select value={ledgerLens} onChange={(event) => setLedgerLens(event.target.value)}>{lensOptions.map((item) => <option key={item}>{item}</option>)}</select>
          <span>{results.length} shown</span>
        </div>
        <div className="ledger-body">
          <div className="evidence-grid">
            {results.map((item, index) => (
              <button key={item.id} onClick={() => onSelect(item)}>
                <span className="evidence-index">{String(index + 1).padStart(2, "0")}</span>
                <span className="evidence-meta">{item.organization} · {item.lens} · {item.tenure}</span>
                <strong>{item.metric}</strong>
                <h3>{item.title}</h3>
                <p>{item.summary}</p>
                <span className="open-case">Trace path <IconArrowNarrowRight size={17} /></span>
              </button>
            ))}
          </div>
          <aside className="ledger-side">
            <div><span className="eyebrow">CAPABILITY FINGERPRINT</span><h3>Broad range, deep growth.</h3>{impactSummary.capability.map(([label, count]) => <p key={label}><span>{label}</span><strong>{count}</strong></p>)}</div>
            <div><span className="eyebrow">THE THINKING</span><h3>89 essays.</h3>{impactSummary.thinking.map(([label, count]) => <p key={label}><span>{label}</span><strong>{count}</strong></p>)}</div>
          </aside>
        </div>
      </section>
    </div>
  );
}

export function App() {
  const [view, setView] = useState(() => {
    const requested = new URLSearchParams(window.location.search).get("view");
    return requested && viewMeta[requested] ? requested : "system";
  });
  const [market, setMarket] = useState("both");
  const [yearStart, setYearStart] = useState(2009);
  const [lens, setLens] = useState("All lenses");
  const [selectedOrganization, setSelectedOrganization] = useState("Praava");
  const [activeEvidenceId, setActiveEvidenceId] = useState("praava-hypergrowth");
  const [ledgerOpen, setLedgerOpen] = useState(false);
  const hero = heroByView[view];
  const visibleProofStats = view === "system" ? proofStats : headlineProofStats;

  const filteredEvidence = useMemo(() => evidence.filter((item) => {
    const matchesMarket = market === "both" || item.market === market || item.market === "both";
    const matchesYear = item.year >= yearStart;
    const matchesLens = lens === "All lenses" || item.lens === lens;
    return matchesMarket && matchesYear && matchesLens;
  }), [market, yearStart, lens]);

  useEffect(() => {
    if (!filteredEvidence.some((item) => item.organization === selectedOrganization)) {
      setSelectedOrganization(filteredEvidence[0]?.organization || "Praava");
    }
  }, [filteredEvidence, selectedOrganization]);

  useEffect(() => {
    const organizationItems = filteredEvidence.filter((item) => item.organization === selectedOrganization);
    if (!organizationItems.some((item) => item.id === activeEvidenceId)) setActiveEvidenceId(organizationItems[0]?.id || filteredEvidence[0]?.id);
  }, [filteredEvidence, selectedOrganization, activeEvidenceId]);

  useEffect(() => {
    const url = new URL(window.location.href);
    url.searchParams.set("view", view);
    window.history.replaceState({}, "", url);
  }, [view]);

  const selectLedgerItem = (item) => {
    setMarket("both");
    setYearStart(2009);
    setLens("All lenses");
    setSelectedOrganization(item.organization);
    setActiveEvidenceId(item.id);
    setView("system");
    setLedgerOpen(false);
  };

  return (
    <div className={`app-shell view-${view}`}>
      <header className="site-header">
        <a className="wordmark" href="https://shafaatalichoyon.com/">Shafaat Choyon<span>.</span></a>
        <a className="back-link" href="https://shafaatalichoyon.com/"><IconArrowLeft size={16} />Back to portfolio</a>
      </header>
      <main>
        <section className="hero-bar">
          <div className="hero-copy">
            <span className="eyebrow">{hero.eyebrow}</span>
            <h1>{hero.title}</h1>
            <p>{hero.description} {hero.emphasis && <strong>{hero.emphasis}</strong>}</p>
            <div className="proof-row">{visibleProofStats.map((item) => <ProofChip key={item.value} item={item} />)}</div>
          </div>
          {view !== "career" && <div className="hero-controls">
            <Segmented value={view} onChange={setView} />
            {view === "system" && <Filters market={market} setMarket={setMarket} yearStart={yearStart} setYearStart={setYearStart} lens={lens} setLens={setLens} />}
          </div>}
        </section>

        <div className="view-stage" key={view}>
        {view === "system" && filteredEvidence.length === 0 ? (
          <section className="empty-state"><IconAdjustmentsHorizontal size={30} /><h2>No evidence matches these filters.</h2><p>Reset the lens or expand the year range to restore the map.</p><button onClick={() => { setLens("All lenses"); setYearStart(2009); setMarket("both"); }}>Reset filters</button></section>
        ) : view === "system" ? (
          <SystemMap filteredEvidence={filteredEvidence} selectedOrganization={selectedOrganization} setSelectedOrganization={setSelectedOrganization} activeEvidenceId={activeEvidenceId} setActiveEvidenceId={setActiveEvidenceId} openLedger={() => setLedgerOpen(true)} />
        ) : view === "atlas" ? (
          <TShapedAtlas selectedOrganization={selectedOrganization} setSelectedOrganization={setSelectedOrganization} openLedger={() => setLedgerOpen(true)} />
        ) : view === "career" ? (
          <CareerJourney openLedger={() => setLedgerOpen(true)} view={view} setView={setView} />
        ) : (
          <TwoMarkets setMarket={setMarket} setView={setView} setSelectedOrganization={setSelectedOrganization} />
        )}
        </div>
      </main>
      <footer className="site-footer"><span>Growth is the deep capability. Health is the deliberate application.</span><a href="https://shafaatalichoyon.com/impact.html">Read the original impact page <IconExternalLink size={15} /></a></footer>
      {ledgerOpen && <EvidenceLedger onClose={() => setLedgerOpen(false)} onSelect={selectLedgerItem} />}
    </div>
  );
}
