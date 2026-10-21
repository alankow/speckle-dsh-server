<template>
  <ViewerControlsButtonToggle
    v-for="pdf in availablePdfs"
    :key="pdf.modelId"
    v-tippy="availablePdfs.length > 1 ? `Télécharger le PDF (${pdf.modelId})` : 'Télécharger le PDF'"
    :icon="FileDown"
    secondary
    @click="openPdf(pdf.url)"
  />
</template>

<script setup lang="ts">
import { FileDown } from 'lucide-vue-next'
import {
  useInjectedViewerLoadedResources,
  useInjectedViewerState
} from '~~/lib/viewer/composables/setup'

// Dushow: bouton "Télécharger le PDF" du modèle.
// Le PDF est attendu à /pdf/<projectId>/<modelId>.pdf (dossier servi par le reverse proxy).
// Le bouton n'apparaît que si le fichier existe.
const PDF_BASE_URL = '/pdf'

const { projectId } = useInjectedViewerState()
const { resourceItems } = useInjectedViewerLoadedResources()

const availablePdfs = ref<Array<{ modelId: string; url: string }>>([])

const modelIds = computed(() => [
  ...new Set(
    resourceItems.value
      .map((i) => i.modelId)
      .filter((id): id is string => typeof id === 'string' && id.length > 0)
  )
])

watch(
  [projectId, modelIds],
  async ([pid, ids]) => {
    const found: Array<{ modelId: string; url: string }> = []
    for (const modelId of ids) {
      const url = `${PDF_BASE_URL}/${pid}/${modelId}.pdf`
      try {
        const res = await fetch(url, { method: 'HEAD' })
        const type = res.headers.get('content-type') || ''
        if (res.ok && type.includes('pdf')) found.push({ modelId, url })
      } catch {
        // pas de PDF pour ce modèle
      }
    }
    availablePdfs.value = found
  },
  { immediate: true }
)

const openPdf = (url: string) => {
  window.open(url, '_blank')
}
</script>
