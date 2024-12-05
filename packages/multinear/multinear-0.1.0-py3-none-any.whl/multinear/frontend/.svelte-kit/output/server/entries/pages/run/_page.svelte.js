import { Z as spread_props, _ as slot, $ as sanitize_props, S as store_get, a5 as copy_payload, a6 as assign_payload, X as unsubscribe_stores, R as pop, W as escape_html, a0 as ensure_array_like, V as stringify, T as attr, P as push } from "../../../chunks/index.js";
import { C as Card, a as Card_header, b as Card_title, c as Card_description } from "../../../chunks/card-title.js";
import { w as getRunDetails, i as TimeAgo, L as Label, I as Input, C as Card_content, T as Table, b as Table_header, d as Table_row, e as Table_head, f as Table_body, h as Table_cell } from "../../../chunks/TimeAgo.js";
import { C as Card_footer } from "../../../chunks/card-footer.js";
import { B as Button } from "../../../chunks/index3.js";
import { J as selectedRunId } from "../../../chunks/projects.js";
import "clsx";
import { formatDuration, intervalToDuration } from "date-fns";
import { f as filterTasks, g as getStatusCounts, S as StatusFilter, a as getTaskStatus, t as truncateInput } from "../../../chunks/tasks.js";
import "../../../chunks/client.js";
import { I as Icon } from "../../../chunks/Icon.js";
function Chevron_right($$payload, $$props) {
  const $$sanitized_props = sanitize_props($$props);
  const iconNode = [["path", { "d": "m9 18 6-6-6-6" }]];
  Icon($$payload, spread_props([
    { name: "chevron-right" },
    $$sanitized_props,
    {
      iconNode,
      children: ($$payload2) => {
        $$payload2.out += `<!---->`;
        slot($$payload2, $$props, "default", {}, null);
        $$payload2.out += `<!---->`;
      },
      $$slots: { default: true }
    }
  ]));
}
function _page($$payload, $$props) {
  push();
  var $$store_subs;
  let filteredTasks, statusCounts;
  let runDetails = null;
  let loading = true;
  let error = null;
  let expandedTaskId = null;
  async function loadRunDetails(id) {
    loading = true;
    error = null;
    try {
      runDetails = await getRunDetails(id);
    } catch (e) {
      error = e instanceof Error ? e.message : "Failed to load run details";
      console.error(e);
    } finally {
      loading = false;
    }
  }
  let statusFilter = "";
  let searchTerm = "";
  {
    if (store_get($$store_subs ??= {}, "$selectedRunId", selectedRunId)) loadRunDetails(store_get($$store_subs ??= {}, "$selectedRunId", selectedRunId));
  }
  filteredTasks = filterTasks(runDetails?.tasks || [], statusFilter, searchTerm);
  statusCounts = getStatusCounts(runDetails?.tasks || []);
  let $$settled = true;
  let $$inner_payload;
  function $$render_inner($$payload2) {
    $$payload2.out += `<div class="container mx-auto p-4"><div class="flex justify-between items-center mb-4"><div class="flex gap-12 items-center"><h1 class="text-3xl font-bold">Run: ${escape_html(store_get($$store_subs ??= {}, "$selectedRunId", selectedRunId).slice(-8))}</h1> `;
    if (runDetails) {
      $$payload2.out += "<!--[-->";
      $$payload2.out += `<span class="text-xl text-gray-500">`;
      TimeAgo($$payload2, { date: runDetails.date });
      $$payload2.out += `<!----></span>`;
    } else {
      $$payload2.out += "<!--[!-->";
    }
    $$payload2.out += `<!--]--></div> `;
    if (runDetails) {
      $$payload2.out += "<!--[-->";
      $$payload2.out += `<div class="flex gap-2 items-center"><span class="text-sm text-gray-500">Project</span> <span class="text-md text-gray-800">${escape_html(runDetails.project.name)}</span></div>`;
    } else {
      $$payload2.out += "<!--[!-->";
    }
    $$payload2.out += `<!--]--></div> `;
    if (loading) {
      $$payload2.out += "<!--[-->";
      $$payload2.out += `<div class="text-center text-gray-500">Loading run details...</div>`;
    } else {
      $$payload2.out += "<!--[!-->";
      if (error) {
        $$payload2.out += "<!--[-->";
        Card($$payload2, {
          class: "border-red-200 bg-red-50",
          children: ($$payload3) => {
            Card_header($$payload3, {
              children: ($$payload4) => {
                Card_title($$payload4, {
                  class: "text-red-800",
                  children: ($$payload5) => {
                    $$payload5.out += `<!---->Error`;
                  },
                  $$slots: { default: true }
                });
                $$payload4.out += `<!----> `;
                Card_description($$payload4, {
                  class: "text-red-600",
                  children: ($$payload5) => {
                    $$payload5.out += `<!---->${escape_html(error)}`;
                  },
                  $$slots: { default: true }
                });
                $$payload4.out += `<!---->`;
              },
              $$slots: { default: true }
            });
            $$payload3.out += `<!----> `;
            Card_footer($$payload3, {
              class: "flex justify-end",
              children: ($$payload4) => {
                Button($$payload4, {
                  variant: "outline",
                  class: "border-red-200 text-red-800 hover:bg-red-100",
                  children: ($$payload5) => {
                    $$payload5.out += `<!---->Try Again`;
                  },
                  $$slots: { default: true }
                });
              },
              $$slots: { default: true }
            });
            $$payload3.out += `<!---->`;
          },
          $$slots: { default: true }
        });
      } else {
        $$payload2.out += "<!--[!-->";
        if (runDetails) {
          $$payload2.out += "<!--[-->";
          $$payload2.out += `<div class="space-y-6">`;
          Card($$payload2, {
            class: "pb-4",
            children: ($$payload3) => {
              Card_header($$payload3, {
                children: ($$payload4) => {
                  Card_description($$payload4, {
                    children: ($$payload5) => {
                      $$payload5.out += `<div class="grid grid-cols-2 md:grid-cols-4 gap-4"><div class="space-y-1"><div class="text-sm text-gray-500">Status</div> <div class="font-semibold">${escape_html(runDetails.status)}</div></div> <div class="space-y-1"><div class="text-sm text-gray-500">Total Tasks</div> <div class="font-semibold">${escape_html(runDetails.tasks.length)}</div></div> <div class="space-y-1"><div class="text-sm text-gray-500">Model</div> <div class="font-semibold">${escape_html(runDetails.details.model || "N/A")}</div></div> <div class="space-y-1">`;
                      Label($$payload5, {
                        for: "search",
                        children: ($$payload6) => {
                          $$payload6.out += `<!---->Search`;
                        },
                        $$slots: { default: true }
                      });
                      $$payload5.out += `<!----> `;
                      Input($$payload5, {
                        id: "search",
                        placeholder: "Search tasks...",
                        get value() {
                          return searchTerm;
                        },
                        set value($$value) {
                          searchTerm = $$value;
                          $$settled = false;
                        }
                      });
                      $$payload5.out += `<!----></div></div> <div class="flex gap-8 items-end mt-4">`;
                      if (runDetails.tasks.length >= 5) {
                        $$payload5.out += "<!--[-->";
                        StatusFilter($$payload5, {
                          get statusFilter() {
                            return statusFilter;
                          },
                          set statusFilter($$value) {
                            statusFilter = $$value;
                            $$settled = false;
                          },
                          statusCounts,
                          totalCount: runDetails.tasks.length
                        });
                      } else {
                        $$payload5.out += "<!--[!-->";
                      }
                      $$payload5.out += `<!--]--></div>`;
                    },
                    $$slots: { default: true }
                  });
                },
                $$slots: { default: true }
              });
            },
            $$slots: { default: true }
          });
          $$payload2.out += `<!----> `;
          Card($$payload2, {
            children: ($$payload3) => {
              Card_content($$payload3, {
                children: ($$payload4) => {
                  Table($$payload4, {
                    class: "-mt-4",
                    children: ($$payload5) => {
                      Table_header($$payload5, {
                        children: ($$payload6) => {
                          Table_row($$payload6, {
                            children: ($$payload7) => {
                              Table_head($$payload7, {});
                              $$payload7.out += `<!----> `;
                              Table_head($$payload7, {
                                children: ($$payload8) => {
                                  $$payload8.out += `<!---->Task ID`;
                                },
                                $$slots: { default: true }
                              });
                              $$payload7.out += `<!----> `;
                              Table_head($$payload7, {
                                children: ($$payload8) => {
                                  $$payload8.out += `<!---->Started`;
                                },
                                $$slots: { default: true }
                              });
                              $$payload7.out += `<!----> `;
                              Table_head($$payload7, {
                                children: ($$payload8) => {
                                  $$payload8.out += `<!---->Duration`;
                                },
                                $$slots: { default: true }
                              });
                              $$payload7.out += `<!----> `;
                              Table_head($$payload7, {
                                children: ($$payload8) => {
                                  $$payload8.out += `<!---->Model`;
                                },
                                $$slots: { default: true }
                              });
                              $$payload7.out += `<!----> `;
                              Table_head($$payload7, {
                                children: ($$payload8) => {
                                  $$payload8.out += `<!---->Input`;
                                },
                                $$slots: { default: true }
                              });
                              $$payload7.out += `<!----> `;
                              Table_head($$payload7, {
                                children: ($$payload8) => {
                                  $$payload8.out += `<!---->Status`;
                                },
                                $$slots: { default: true }
                              });
                              $$payload7.out += `<!----> `;
                              Table_head($$payload7, {
                                children: ($$payload8) => {
                                  $$payload8.out += `<!---->Score`;
                                },
                                $$slots: { default: true }
                              });
                              $$payload7.out += `<!---->`;
                            },
                            $$slots: { default: true }
                          });
                        },
                        $$slots: { default: true }
                      });
                      $$payload5.out += `<!----> `;
                      Table_body($$payload5, {
                        children: ($$payload6) => {
                          const each_array = ensure_array_like(filteredTasks);
                          $$payload6.out += `<!--[-->`;
                          for (let $$index_4 = 0, $$length = each_array.length; $$index_4 < $$length; $$index_4++) {
                            let task = each_array[$$index_4];
                            const isExpanded = expandedTaskId === task.id;
                            const { isPassed, statusClass } = getTaskStatus(task);
                            Table_row($$payload6, {
                              "data-task-id": task.id,
                              class: `cursor-pointer ${statusClass}`,
                              children: ($$payload7) => {
                                Table_cell($$payload7, {
                                  class: "w-4",
                                  children: ($$payload8) => {
                                    Button($$payload8, {
                                      variant: "ghost",
                                      size: "sm",
                                      class: "h-4 w-4 p-0",
                                      children: ($$payload9) => {
                                        Chevron_right($$payload9, {
                                          class: `h-4 w-4 transition-transform duration-200 text-gray-400
                                                ${stringify(isExpanded ? "rotate-90" : "")}`
                                        });
                                      },
                                      $$slots: { default: true }
                                    });
                                  },
                                  $$slots: { default: true }
                                });
                                $$payload7.out += `<!----> `;
                                Table_cell($$payload7, {
                                  class: "font-medium font-mono",
                                  children: ($$payload8) => {
                                    $$payload8.out += `<!---->${escape_html(task.id.slice(-8))}`;
                                  },
                                  $$slots: { default: true }
                                });
                                $$payload7.out += `<!----> `;
                                Table_cell($$payload7, {
                                  children: ($$payload8) => {
                                    TimeAgo($$payload8, { date: task.created_at });
                                  },
                                  $$slots: { default: true }
                                });
                                $$payload7.out += `<!----> `;
                                Table_cell($$payload7, {
                                  children: ($$payload8) => {
                                    if (task.finished_at) {
                                      $$payload8.out += "<!--[-->";
                                      $$payload8.out += `${escape_html(formatDuration(
                                        intervalToDuration({
                                          start: new Date(task.created_at),
                                          end: new Date(task.finished_at)
                                        }),
                                        { format: ["minutes", "seconds"] }
                                      ))}`;
                                    } else {
                                      $$payload8.out += "<!--[!-->";
                                      $$payload8.out += `-`;
                                    }
                                    $$payload8.out += `<!--]-->`;
                                  },
                                  $$slots: { default: true }
                                });
                                $$payload7.out += `<!----> `;
                                Table_cell($$payload7, {
                                  children: ($$payload8) => {
                                    $$payload8.out += `<!---->${escape_html(task.task_details?.model || "-")}`;
                                  },
                                  $$slots: { default: true }
                                });
                                $$payload7.out += `<!----> `;
                                Table_cell($$payload7, {
                                  class: "max-w-xs",
                                  children: ($$payload8) => {
                                    $$payload8.out += `<!---->${escape_html(truncateInput(task.task_input))}`;
                                  },
                                  $$slots: { default: true }
                                });
                                $$payload7.out += `<!----> `;
                                Table_cell($$payload7, {
                                  children: ($$payload8) => {
                                    $$payload8.out += `<span${attr("class", `inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium
                                            ${task.status === "completed" ? "bg-green-100 text-green-800" : task.status === "failed" ? "bg-red-100 text-red-800" : "bg-gray-100 text-gray-800"}`)}>${escape_html(task.status)}</span>`;
                                  },
                                  $$slots: { default: true }
                                });
                                $$payload7.out += `<!----> `;
                                Table_cell($$payload7, {
                                  children: ($$payload8) => {
                                    $$payload8.out += `<div class="w-full bg-gray-200 rounded-sm h-4 dark:bg-gray-700 overflow-hidden flex"><div${attr("class", `h-4 min-w-[5px] ${stringify(isPassed ? "bg-green-600" : "bg-red-600")}`)}${attr("style", `width: ${stringify((task.eval_score * 100).toFixed(0))}%`)}></div></div> <div class="text-center text-xs font-medium">${escape_html((task.eval_score * 100).toFixed(0))}%</div>`;
                                  },
                                  $$slots: { default: true }
                                });
                                $$payload7.out += `<!---->`;
                              },
                              $$slots: { default: true }
                            });
                            $$payload6.out += `<!----> `;
                            if (isExpanded) {
                              $$payload6.out += "<!--[-->";
                              Table_row($$payload6, {
                                class: "bg-gray-50 hover:bg-gray-50",
                                children: ($$payload7) => {
                                  Table_cell($$payload7, {
                                    colspan: 8,
                                    class: "border-t border-gray-100",
                                    children: ($$payload8) => {
                                      $$payload8.out += `<div class="p-4 grid grid-cols-1 md:grid-cols-2 gap-6"><div class="space-y-4 pr-12 border-r border-gray-200"><div class="flex justify-between items-center mb-2"><h4 class="font-semibold text-lg">Task</h4> <div class="text-sm text-gray-800">Duration: `;
                                      if (task.executed_at) {
                                        $$payload8.out += "<!--[-->";
                                        $$payload8.out += `${escape_html(formatDuration(
                                          intervalToDuration({
                                            start: new Date(task.created_at),
                                            end: new Date(task.executed_at)
                                          }),
                                          { format: ["minutes", "seconds"] }
                                        ))}`;
                                      } else {
                                        $$payload8.out += "<!--[!-->";
                                        $$payload8.out += `-`;
                                      }
                                      $$payload8.out += `<!--]--></div></div> `;
                                      if (task.task_input) {
                                        $$payload8.out += "<!--[-->";
                                        $$payload8.out += `<div><h5 class="font-semibold mb-1">Input</h5> <div class="text-sm bg-white p-2 rounded border overflow-auto" style="white-space: pre-wrap;">${escape_html(typeof task.task_input === "object" && "str" in task.task_input ? task.task_input.str : JSON.stringify(task.task_input, null, 2))}</div></div>`;
                                      } else {
                                        $$payload8.out += "<!--[!-->";
                                      }
                                      $$payload8.out += `<!--]--> `;
                                      if (task.task_output) {
                                        $$payload8.out += "<!--[-->";
                                        $$payload8.out += `<div><div class="flex justify-between items-center mb-1"><h5 class="font-semibold">Output</h5> `;
                                        Button($$payload8, {
                                          variant: "outline",
                                          size: "sm",
                                          class: "text-sm bg-gray-200 hover:bg-gray-300 dark:hover:bg-gray-700 transition-colors",
                                          children: ($$payload9) => {
                                            $$payload9.out += `<!---->Cross-Compare`;
                                          },
                                          $$slots: { default: true }
                                        });
                                        $$payload8.out += `<!----></div> <div class="text-sm bg-white p-2 rounded border overflow-auto" style="white-space: pre-wrap;">${escape_html(typeof task.task_output === "object" && "str" in task.task_output ? task.task_output.str : JSON.stringify(task.task_output, null, 2))}</div></div>`;
                                      } else {
                                        $$payload8.out += "<!--[!-->";
                                      }
                                      $$payload8.out += `<!--]--> `;
                                      if (task.task_details) {
                                        $$payload8.out += "<!--[-->";
                                        const each_array_1 = ensure_array_like(Object.entries(task.task_details));
                                        $$payload8.out += `<div><h5 class="font-semibold mb-1">Details</h5> <!--[-->`;
                                        for (let $$index = 0, $$length2 = each_array_1.length; $$index < $$length2; $$index++) {
                                          let [key, value] = each_array_1[$$index];
                                          $$payload8.out += `<div class="mb-1 pl-2"><h6 class="font-semibold">${escape_html(key)}</h6> <div class="text-sm bg-white p-2 rounded border overflow-auto" style="white-space: pre-wrap;">${escape_html(typeof value === "string" ? value : JSON.stringify(value, null, 2))}</div></div>`;
                                        }
                                        $$payload8.out += `<!--]--></div>`;
                                      } else {
                                        $$payload8.out += "<!--[!-->";
                                      }
                                      $$payload8.out += `<!--]--> `;
                                      if (task.task_logs) {
                                        $$payload8.out += "<!--[-->";
                                        const each_array_2 = ensure_array_like(task.task_logs.logs);
                                        $$payload8.out += `<div><h5 class="font-semibold mb-1">Logs</h5> <details><summary class="cursor-pointer text-blue-500">Show Logs</summary> <table class="text-sm bg-white p-2 rounded border overflow-auto w-full mt-2"><thead><tr><th class="text-left">Level</th><th class="text-left">Timestamp</th><th class="text-left">Message</th></tr></thead><tbody><!--[-->`;
                                        for (let $$index_1 = 0, $$length2 = each_array_2.length; $$index_1 < $$length2; $$index_1++) {
                                          let log = each_array_2[$$index_1];
                                          $$payload8.out += `<tr><td>${escape_html(log.level)}</td><td>${escape_html(new Date(log.timestamp * 1e3).toLocaleString())}</td><td>${escape_html(log.message)}</td></tr>`;
                                        }
                                        $$payload8.out += `<!--]--></tbody></table></details></div>`;
                                      } else {
                                        $$payload8.out += "<!--[!-->";
                                      }
                                      $$payload8.out += `<!--]--></div> <div class="space-y-4 pl-4"><div class="flex justify-between items-center mb-2"><h4 class="font-semibold text-lg">Evaluation</h4> <div class="flex items-center gap-4"><div class="text-sm text-gray-800">Duration: `;
                                      if (task.evaluated_at) {
                                        $$payload8.out += "<!--[-->";
                                        $$payload8.out += `${escape_html(formatDuration(
                                          intervalToDuration({
                                            start: new Date(task.executed_at),
                                            end: new Date(task.evaluated_at)
                                          }),
                                          { format: ["minutes", "seconds"] }
                                        ))}`;
                                      } else {
                                        $$payload8.out += "<!--[!-->";
                                        $$payload8.out += `-`;
                                      }
                                      $$payload8.out += `<!--]--></div> <div class="text-sm text-gray-800">Score: ${escape_html((task.eval_score * 100).toFixed(0))}%</div> <div${attr("class", `px-4 py-1 rounded-lg font-semibold
                                                                ${task.eval_passed ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`)}>${escape_html(task.eval_passed ? "PASSED" : "FAILED")}</div></div></div> `;
                                      if (task.eval_details?.evaluations) {
                                        $$payload8.out += "<!--[-->";
                                        $$payload8.out += `<div>`;
                                        Table($$payload8, {
                                          children: ($$payload9) => {
                                            Table_header($$payload9, {
                                              children: ($$payload10) => {
                                                Table_row($$payload10, {
                                                  children: ($$payload11) => {
                                                    Table_head($$payload11, {
                                                      children: ($$payload12) => {
                                                        $$payload12.out += `<!---->Criteria`;
                                                      },
                                                      $$slots: { default: true }
                                                    });
                                                    $$payload11.out += `<!----> `;
                                                    Table_head($$payload11, {
                                                      class: "w-24 text-center",
                                                      children: ($$payload12) => {
                                                        $$payload12.out += `<!---->Score`;
                                                      },
                                                      $$slots: { default: true }
                                                    });
                                                    $$payload11.out += `<!---->`;
                                                  },
                                                  $$slots: { default: true }
                                                });
                                              },
                                              $$slots: { default: true }
                                            });
                                            $$payload9.out += `<!----> `;
                                            Table_body($$payload9, {
                                              children: ($$payload10) => {
                                                const each_array_3 = ensure_array_like(task.eval_details.evaluations);
                                                $$payload10.out += `<!--[-->`;
                                                for (let $$index_2 = 0, $$length2 = each_array_3.length; $$index_2 < $$length2; $$index_2++) {
                                                  let ev = each_array_3[$$index_2];
                                                  Table_row($$payload10, {
                                                    children: ($$payload11) => {
                                                      Table_cell($$payload11, {
                                                        children: ($$payload12) => {
                                                          $$payload12.out += `<div class="space-y-1"><div>${escape_html(ev.criterion)}</div> <div class="text-sm text-gray-500">${escape_html(ev.rationale)}</div></div>`;
                                                        },
                                                        $$slots: { default: true }
                                                      });
                                                      $$payload11.out += `<!----> `;
                                                      Table_cell($$payload11, {
                                                        class: "text-center",
                                                        children: ($$payload12) => {
                                                          $$payload12.out += `<div${attr("class", `inline-flex items-center justify-center w-12 h-12 rounded-full ${stringify(ev.score >= 1 ? "bg-green-100 text-green-800" : ev.score > 0 ? "bg-yellow-100 text-yellow-800" : "bg-red-100 text-red-800")}`)}>${escape_html((ev.score * 100).toFixed(0))}%</div>`;
                                                        },
                                                        $$slots: { default: true }
                                                      });
                                                      $$payload11.out += `<!---->`;
                                                    },
                                                    $$slots: { default: true }
                                                  });
                                                }
                                                $$payload10.out += `<!--]-->`;
                                              },
                                              $$slots: { default: true }
                                            });
                                            $$payload9.out += `<!---->`;
                                          },
                                          $$slots: { default: true }
                                        });
                                        $$payload8.out += `<!----></div>`;
                                      } else {
                                        $$payload8.out += "<!--[!-->";
                                      }
                                      $$payload8.out += `<!--]--> `;
                                      if (task.eval_details) {
                                        $$payload8.out += "<!--[-->";
                                        const each_array_4 = ensure_array_like(Object.entries(task.eval_details));
                                        $$payload8.out += `<div><h5 class="font-semibold mb-1">Details</h5> <!--[-->`;
                                        for (let $$index_3 = 0, $$length2 = each_array_4.length; $$index_3 < $$length2; $$index_3++) {
                                          let [key, value] = each_array_4[$$index_3];
                                          if (key !== "evaluations") {
                                            $$payload8.out += "<!--[-->";
                                            $$payload8.out += `<div class="mb-1 pl-2"><h6 class="font-semibold">${escape_html(key)}</h6> <div class="text-sm bg-white p-2 rounded border overflow-auto" style="white-space: pre-wrap;">${escape_html(typeof value === "string" ? value : JSON.stringify(value, null, 2))}</div></div>`;
                                          } else {
                                            $$payload8.out += "<!--[!-->";
                                          }
                                          $$payload8.out += `<!--]-->`;
                                        }
                                        $$payload8.out += `<!--]--></div>`;
                                      } else {
                                        $$payload8.out += "<!--[!-->";
                                      }
                                      $$payload8.out += `<!--]--></div></div>`;
                                    },
                                    $$slots: { default: true }
                                  });
                                },
                                $$slots: { default: true }
                              });
                            } else {
                              $$payload6.out += "<!--[!-->";
                            }
                            $$payload6.out += `<!--]-->`;
                          }
                          $$payload6.out += `<!--]-->`;
                        },
                        $$slots: { default: true }
                      });
                      $$payload5.out += `<!---->`;
                    },
                    $$slots: { default: true }
                  });
                },
                $$slots: { default: true }
              });
            },
            $$slots: { default: true }
          });
          $$payload2.out += `<!----></div>`;
        } else {
          $$payload2.out += "<!--[!-->";
          $$payload2.out += `<div class="text-center text-gray-500">No run found</div>`;
        }
        $$payload2.out += `<!--]-->`;
      }
      $$payload2.out += `<!--]-->`;
    }
    $$payload2.out += `<!--]--></div>`;
  }
  do {
    $$settled = true;
    $$inner_payload = copy_payload($$payload);
    $$render_inner($$inner_payload);
  } while (!$$settled);
  assign_payload($$payload, $$inner_payload);
  if ($$store_subs) unsubscribe_stores($$store_subs);
  pop();
}
export {
  _page as default
};
