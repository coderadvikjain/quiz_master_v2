<template>
  <div
    class="modal fade show"
    tabindex="-1"
    style="display: block; background: rgba(0, 0, 0, 0.4); backdrop-filter: blur(3px);"
    role="dialog"
    @click.self="$emit('close')">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content border-0 shadow-lg rounded-4 overflow-hidden">
        <div class="modal-header text-white bg-gradient-user px-4 py-3">
          <h5 class="modal-title fw-bold">🙍‍♂️ Profile Details</h5>
          <button
            type="button"
            class="btn-close btn-close-white"
            @click="$emit('close')"
            aria-label="Close"
            title="Close">
          </button>
        </div>
        <div class="modal-body px-4 py-4 bg-white">
          <h4 class="fw-bold text-primary border-bottom pb-3 mb-4 d-flex align-items-center">
            <i class="bi bi-person-fill me-2 fs-4"></i> Profile Overview
          </h4>
          <div class="row row-cols-1 row-cols-md-2 g-4 mb-5">
            <div class="col" v-for="(label, key) in {
              'Full Name': user.full_name,
              'Email': user.email,
              'Qualification': user.qualification || 'N/A',
              'Date of Birth': user.dob || 'N/A'}" :key="key">
              <div class="border rounded-3 p-3 overview-box bg-light h-100">
                <div class="text-muted small">{{ key }}</div>
                <div
                  class="fs-6 fw-semibold text-my text-dark"
                  :class="{ 'text-capitalize': key === 'Full Name'}"
                  :style="{
                    'white-space': 'nowrap',
                    'overflow': 'hidden',
                    'text-overflow': 'ellipsis',
                    'display': 'block'
                  }"
                  :title="label">
                  {{ label }}
                </div>
              </div>
            </div>
          </div>

          <!-- Earned Badges -->
          <div class="mb-5">
            <h5 class="text-success fw-bold mb-3 d-flex align-items-center">
              <i class="bi bi-award-fill me-2 fs-5"></i> Earned Badges
            </h5>
            <div v-if="userBadges.length > 0" class="d-flex flex-wrap gap-4">
              <div
                v-for="(badge, index) in allBadges.filter(b => userBadges.includes(b.name))"
                :key="index"
                class="text-center p-3 rounded-4 border overview-box bg-light shadow-sm"
                style="width: 110px;">
                <div class="fs-1 mb-2">{{ badge.emoji }}</div>
                <div class="fw-semibold small mytext text-dark">{{ badge.name }}</div>
              </div>
            </div>
            <div v-else class="text-muted fst-italic">
              No badges earned yet.
            </div>
          </div>

          <!-- Performance Overview -->
          <div>
            <h5 class="text-warning fw-bold mb-3 d-flex align-items-center">
              <i class="bi bi-graph-up-arrow me-2 fs-5"></i> Performance Overview
            </h5>
            <div class="d-flex justify-content-between align-items-center p-3 border rounded-3 overview-box bg-light shadow-sm flex-column flex-md-row gap-3">
              <div class="mytext text-dark text-center text-md-start">
                Download your quiz performance &<br>summary instantly!
              </div>
              <button
                class="btn btn-outline-warning rounded-pill px-3 py-1 fw-semibold small d-flex align-items-center"
                :disabled="exporting"
                @click="downloadReport">
                <span v-if="exporting" class="spinner-border spinner-border-sm me-2" role="status"></span>
                {{ exporting ? 'Preparing...' : 'Get Report' }}
              </button>
            </div>
          </div>
        </div>
        <div class="modal-footer bg-light px-4 py-3 d-flex justify-content-end">
          <button class="btn btn-secondary fw-semibold" @click="$emit('close')">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { exportcsv, checkExportStatus, downloadExportedCSV } from '@/services/api';

export default {
  name: 'ProfileModal',
  props: {
    user: {
      type: Object,
      required: true,
    },
    scores: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
  data() {
    return {
      exporting: false,
    };
  },
  methods: {
    async downloadReport() {
      this.exporting = true;
      try {
        const exportResponse = await exportcsv();
        const taskId = exportResponse.task_id;

        this.$toast?.success("Export started. Preparing your file...");

        const pollStatus = async () => {
          const statusRes = await checkExportStatus(taskId);
          if (statusRes.status === 'success') {
            return statusRes.filename;
          } else if (statusRes.status === 'processing') {
            await new Promise(resolve => setTimeout(resolve, 1500));
            return pollStatus();
          } else {
            throw new Error("Export failed");
          }
        };

        const filename = await pollStatus();

        const fileRes = await downloadExportedCSV(filename);
        const blob = new Blob([fileRes.data], { type: 'text/csv' });

        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        this.$toast?.success("Export ready! File downloaded.");
        alert('Your quiz export is ready!');
      } catch (err) {
        console.error(err);
        this.$toast?.error("Failed to export the report.");
      } finally {
        this.exporting = false;
      }
    },
  },
  computed: {
    userBadges() {
      if (!Array.isArray(this.scores)) return [];

      const count = this.scores.length;
      const percentages = this.scores.map(s => {
        const scored = s.total_scored || 0;
        const total = s.total_questions || 1;
        return (scored / total) * 100;
      });

      const allAbove90 = percentages.length > 0 && percentages.every(m => m >= 90);
      const allAbove50 = percentages.length > 0 && percentages.every(m => m >= 50);
      const badges = [];

      if (count >= 2) badges.push('Quiz Master');
      if (count >= 25) badges.push('Frequent Quiz Taker');
      if (count >= 50) badges.push('Quiz Enthusiast');
      if (count >= 75) badges.push('Quiz Champion');
      if (count >= 100) badges.push('Quiz Guru');
      if (count >= 1000) badges.push('Quiz Connoisseur');
      if (count >= 2000) badges.push('Quiz King');

      if (allAbove90 && count >= 2) badges.push('Quiz Virtuoso');
      else if (allAbove50 && count >= 2) badges.push('Consistent Performer');
      if (allAbove90 && count >= 25) badges.push('Quiz Maestro');
      else if (allAbove50 && count >= 25) badges.push('Reliable Performer');
      if (allAbove90 && count >= 50) badges.push('Quiz Mastermind');
      else if (allAbove50 && count >= 50) badges.push('Consistent Achiever');
      if (allAbove90 && count >= 75) badges.push('Quiz God');
      else if (allAbove50 && count >= 75) badges.push('Steady Achiever');
      if (allAbove90 && count >= 100) badges.push('Quiz Deity');
      else if (allAbove50 && count >= 100) badges.push('Reliable Contributor');
      if (allAbove90 && count >= 1000) badges.push('Quiz Immortal');
      else if (allAbove50 && count >= 1000) badges.push('Steady Legend');
      if (allAbove90 && count >= 2000) badges.push('Quiz Genius');
      else if (allAbove50 && count >= 2000) badges.push('Steady Titan');

      return badges;
    },
    allBadges() {
      return [
        { name: 'Quiz Master', emoji: '🏹' },
        { name: 'Frequent Quiz Taker', emoji: '🧩' },
        { name: 'Quiz Enthusiast', emoji: '⚡' },
        { name: 'Quiz Champion', emoji: '🏅' },
        { name: 'Quiz Guru', emoji: '💯' },
        { name: 'Quiz Connoisseur', emoji: '🎯' },
        { name: 'Quiz King', emoji: '🔥' },
        { name: 'Quiz Virtuoso', emoji: '💡' },
        { name: 'Quiz Maestro', emoji: '🏅' },
        { name: 'Quiz Mastermind', emoji: '🧠' },
        { name: 'Quiz God', emoji: '🥉' },
        { name: 'Quiz Deity', emoji: '🥈' },
        { name: 'Quiz Immortal', emoji: '🥇' },
        { name: 'Quiz Genius', emoji: '👑' },
        { name: 'Consistent Performer', emoji: '🎓' },
        { name: 'Reliable Performer', emoji: '🪄' },
        { name: 'Consistent Achiever', emoji: '🏅' },
        { name: 'Steady Achiever', emoji: '🚀' },
        { name: 'Reliable Contributor', emoji: '💪' },
        { name: 'Steady Legend', emoji: '🧙‍♂️' },
        { name: 'Steady Titan', emoji: '🏆' },
      ];
    },
  },
};
</script>

<style scoped>
.bg-gradient-user {
  background: linear-gradient(135deg, #36d1dc, #5b86e5);
}
</style>