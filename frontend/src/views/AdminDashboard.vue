<template>
  <div class="container admin-dashboard">
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <br/><br/>
    <div class="row">
      <div v-for="subject in subjects" :key="subject.id" class="col-md-6 mb-4">
        <div class="subject-box rounded border shadow p-4 bg-white">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="mb-0 text-primary">{{ capitalizeWords(subject.name) }}</h5>
            <div>
              <button class="btn btn-sm btn-link text-success" @click="openEditSubjectModal(subject)" title="Edit Course">
                <i class="bi bi-pencil-fill"></i>
              </button>
              <button class="btn btn-sm btn-link text-danger" @click="confirmDeleteSubject(subject.id)" title="Delete Course">
                <i class="bi bi-trash-fill"></i>
              </button>
            </div>
          </div>
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light" style="position: sticky; top: 0; z-index: 2; background-color: white;">
              <tr>
                <th class="ps-4">Chapter Name</th>
                <th class="text-end pe-4">Actions</th>
              </tr>
            </thead>
          </table>
          <div style="max-height: 120px; overflow-y: auto;" class="scroll-chapter-body border-top">
            <table class="table table-hover align-middle mb-0">
              <tbody>
                <tr v-if="!chapters[subject.id]?.length">
                  <td colspan="2" class="text-center text-muted">No chapter(s) are available yet!!</td>
                </tr>
                <tr v-for="chapter in chapters[subject.id]" :key="chapter.id">
                 <td class="ps-4">
                    <router-link 
                      :to="`/quizzes/${chapter.id}`" 
                      class="text-decoration-none text-my">
                      {{ capitalizeWords(chapter.name) }}
                    </router-link>
                  </td>
                  <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary me-2" @click="openEditChapterModal(chapter)" title="Edit Chapter">
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" @click="confirmDeleteChapter(chapter.id)" title="Delete Chapter">
                      <i class="bi bi-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="text-center mt-3">
            <button class="btn btn-sm btn-warning shadow-sm" @click="openAddChapterModal(subject.id)" title="Add Chapter">
              <i class="bi bi-file-earmark-plus me-1"></i> Add Chapter
            </button>
          </div>
        </div>
      </div>
    </div>
    <button
      class="btn btn-gradient-primary rounded-circle position-fixed shadow-lg d-flex align-items-center justify-content-center"
      style="width: 60px; height: 60px; bottom: 30px; right: 30px; font-size: 32px; transition: all 0.3s ease;"
      @click="openAddSubjectModal"
      title="Add Course"
      data-bs-placement="left">
      <i class="bi bi-journal-plus"></i>
    </button>
  </div>
  <div v-if="subjects.length === 0" class="text-center text-muted py-5 fs-5">
    No subjects found. Please add a subject first.
  </div>

  <AddSubjectModal
    v-if="showAddSubjectModal"
    @close="closeAddSubjectModal"
    @added="handleSubjectAdded"
  />

  <EditSubjectModal
    v-if="showEditSubjectModal"
    :subject="editingSubject"
    @close="closeEditSubjectModal"
    @updated="handleSubjectUpdated"
  />

  <AddChapterModal
    v-if="showAddChapterModal"
    :visible="showAddChapterModal"
    :subjectId="currentSubjectId"
    @close="closeAddChapterModal"
    @added="handleChapterAdded"
  />

  <EditChapterModal
    v-if="showEditChapterModal"
    :chapter="editingChapter"
    @close="closeEditChapterModal"
    @updated="handleChapterUpdated"
  />
</template>

<script>
import { ref, onMounted, inject, watch } from 'vue';
import {
  getSubjects,
  deleteSubject,
  getChapters,
  deleteChapter,
  addSubject,
  addChapter,
  updateSubject,
  updateChapter,
} from '@/services/api';
import AddSubjectModal from '@/components/AddSubjectModal.vue';
import EditSubjectModal from '@/components/EditSubjectModal.vue';
import AddChapterModal from '@/components/AddChapterModal.vue';
import EditChapterModal from '@/components/EditChapterModal.vue';

export default {
  name: 'AdminDashboard',
  components: {
    AddSubjectModal,
    EditSubjectModal,
    AddChapterModal,
    EditChapterModal,
  },
  setup() {
    const subjects = ref([]);
    const allSubjects = ref([]);
    const chapters = ref({});
    const allChapters = ref({});
    const loading = ref(false);
    const showAddSubjectModal = ref(false);
    const showAddChapterModal = ref(false);
    const currentSubjectId = ref(null);
    const showEditSubjectModal = ref(false);
    const editingSubject = ref(null);
    const showEditChapterModal = ref(false);
    const editingChapter = ref(null);
    const searchQuery = inject('searchQuery');

    onMounted(() => {
      document.title = 'StudiQ | Dashboard';
      fetchSubjectsAndChapters();
    });

    async function fetchSubjectsAndChapters() {
      loading.value = true;
      try {
        const response = await getSubjects();
        subjects.value = response.subjects;
        allSubjects.value = response.subjects;
        
        const chaptersMap = {};
        const allChaptersMap = {};
        for (const subj of response.subjects) {
          const chapterResponse = await getChapters(subj.id);
          chaptersMap[subj.id] = chapterResponse.chapters || [];
          allChaptersMap[subj.id] = chapterResponse.chapters || [];
        }
        chapters.value = chaptersMap;
        allChapters.value = allChaptersMap;
      } catch (err) {
        console.error('Error loading subjects/chapters:', err);
      } finally {
        loading.value = false;
      }
    }

    watch(searchQuery, (newQuery) => {
      if (!newQuery) {
        subjects.value = allSubjects.value;
        chapters.value = allChapters.value;
        return;
      }
      const query = typeof newQuery === 'string' ? newQuery.toLowerCase() : '';
      const filteredSubjects = allSubjects.value.filter(subject => {
        const subjectMatch = subject.name.toLowerCase().includes(query);
        const subjectChapters = allChapters.value[subject.id] || [];
        const matchingChapters = subjectChapters.filter(ch =>
          ch.name.toLowerCase().includes(query)
        );
        if (subjectMatch || matchingChapters.length > 0) {
          return true;
        }
        return false;
      });
      const updatedChaptersMap = {};
      filteredSubjects.forEach(subject => {
        const allChaps = allChapters.value[subject.id] || [];
        updatedChaptersMap[subject.id] = allChaps.filter(ch =>
          ch.name.toLowerCase().includes(query)
        );
      });
      subjects.value = filteredSubjects;
      chapters.value = updatedChaptersMap;
    });

    async function handleSubjectAdded(subject) {
      try {
        await addSubject(subject);
        closeAddSubjectModal();
        await fetchSubjectsAndChapters();
      } catch (err) {
        alert(err.response?.data?.msg || err.message);
      }
    }

    async function handleSubjectUpdated(updatedSubject) {
      try {
        await updateSubject(updatedSubject.id, updatedSubject);
        closeEditSubjectModal();
        await fetchSubjectsAndChapters();
      } catch (err) {
        alert(err.response?.data?.msg || err.message);
      }
    }

    async function handleChapterAdded(chapter) {
      try {
        await addChapter(chapter);
        closeAddChapterModal();
        await fetchSubjectsAndChapters();
      } catch (err) {
        alert(err.response?.data?.msg || err.message);
      }
    }

    async function handleChapterUpdated(updatedChapter) {
      try {
        await updateChapter(updatedChapter.id, updatedChapter);
        closeEditChapterModal();
        await fetchSubjectsAndChapters();
      } catch (err) {
        alert(err.response?.data?.msg || err.message);
      }
    }

    async function confirmDeleteSubject(id) {
      if (confirm("You're about to remove this course. Are you sure?")) {
        try {
          await deleteSubject(id);
          await fetchSubjectsAndChapters();
        } catch {
          alert('Failed to delete subject');
        }
      }
    }

    async function confirmDeleteChapter(id) {
      if (confirm("You're about to remove this chapter. Are you sure?")) {
        try {
          await deleteChapter(id);
          await fetchSubjectsAndChapters();
        } catch {
          alert('Failed to delete chapter');
        }
      }
    }

    function capitalizeWords(text) {
      return text.replace(/\b\w/g, char => char.toUpperCase());
    }
    function openAddSubjectModal() {
      showAddSubjectModal.value = true;
    }
    function closeAddSubjectModal() {
      showAddSubjectModal.value = false;
    }
    function openEditSubjectModal(subject) {
      editingSubject.value = subject;
      showEditSubjectModal.value = true;
    }
    function closeEditSubjectModal() {
      showEditSubjectModal.value = false;
      editingSubject.value = null;
    }
    function openAddChapterModal(subjectId) {
      currentSubjectId.value = subjectId;
      showAddChapterModal.value = true;
    }
    function closeAddChapterModal() {
      showAddChapterModal.value = false;
      currentSubjectId.value = null;
    }
    function openEditChapterModal(chapter) {
      editingChapter.value = chapter;
      showEditChapterModal.value = true;
    }
    function closeEditChapterModal() {
      showEditChapterModal.value = false;
      editingChapter.value = null;
    }

    return {
      subjects,
      chapters,
      loading,
      openAddSubjectModal,
      closeAddSubjectModal,
      openEditSubjectModal,
      closeEditSubjectModal,
      openAddChapterModal,
      closeAddChapterModal,
      openEditChapterModal,
      closeEditChapterModal,
      confirmDeleteSubject,
      confirmDeleteChapter,
      handleSubjectAdded,
      handleSubjectUpdated,
      handleChapterAdded,
      handleChapterUpdated,
      capitalizeWords,
      currentSubjectId,
      showAddSubjectModal,
      showEditSubjectModal,
      showAddChapterModal,
      showEditChapterModal,
      editingSubject,
      editingChapter,
    };
  },
};
</script>

<style scoped>
.subject-box {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.subject-box:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}
button.btn i {
  transition: transform 0.2s ease;
}
button.btn:hover i {
  transform: scale(1.2);
}
.btn-warning:hover {
  background-color: #f7b731;
  color: white;
  transform: translateY(-1px);
}
.btn-gradient-primary {
  background-image: linear-gradient(135deg,rgb(254, 114, 79),rgb(237, 254, 0));
  color: white;
  border: none;
}
.btn-gradient-primary:hover {
  background-image: linear-gradient(135deg,rgb(182, 254, 0),rgb(251, 254, 79));
  transform: scale(1.1);
  box-shadow: 0 12px 24px rgba(0, 242, 254, 0.5);
}
.btn-gradient-primary:focus {
  outline: none;
  box-shadow: 0 0 0 0.25rem rgba(254, 213, 79, 0.4);
}
.scroll-chapter-body::-webkit-scrollbar {
  width: 6px;
}
.scroll-chapter-body::-webkit-scrollbar-thumb {
  background: #dee2e6;
  border-radius: 4px;
}
.text-my{
  color:rgb(0, 0, 0);
}
</style>