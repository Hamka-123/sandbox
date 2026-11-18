import jenkins.model.Jenkins
import hudson.model.FreeStyleProject
import hudson.model.ParametersDefinitionProperty
import hudson.model.StringParameterDefinition
import hudson.model.ChoiceParameterDefinition
import hudson.model.BooleanParameterDefinition
import hudson.model.labels.LabelAtom
import hudson.tasks.Shell
import hudson.tasks.ArtifactArchiver

def instance = Jenkins.get()
def jobName = 'lesson9-audit-worker'

def job = instance.getItem(jobName)
if (job == null) {
    job = instance.createProject(FreeStyleProject, jobName)
    println "CREATED_NEW_JOB: ${jobName}"
} else {
    println "UPDATED_EXISTING_JOB: ${jobName}"
}

job.setAssignedLabel(new LabelAtom('built-in'))

job.removeProperty(ParametersDefinitionProperty.class)
def envParam = new ChoiceParameterDefinition('TARGET_ENV', ['dev', 'staging', 'prod'] as String[], 'Target deployment environment')
def reqParam = new StringParameterDefinition('REQUEST_ID', 'REQ-000', 'Tracking ID from upstream orchestrator')
def failParam = new BooleanParameterDefinition('FORCE_FAIL', false, 'Simulate a worker crash for testing')
job.addProperty(new ParametersDefinitionProperty(envParam, reqParam, failParam))

String decodedScript = new String("IyEvdXNyL2Jpbi9lbnYgYmFzaApzZXQgLWV1byBwaXBlZmFpbAoKZWNobyAiPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSIKZWNobyAiICBMRVNTT04gOSBXT1JLRVI6IEFVRElUICYgTUVUQURBVEEgR0VORVJBVE9SIgplY2hvICI9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09IgoKVEFSR0VUX0VOVj0iJHtUQVJHRVRfRU5WOi1zdGFnaW5nfSIKUkVRVUVTVF9JRD0iJHtSRVFVRVNUX0lEOi11bmtub3dufSIKRk9SQ0VfRkFJTD0iJHtGT1JDRV9GQUlMOi1mYWxzZX0iCgplY2hvICItLT4gRW52aXJvbm1lbnQgOiAke1RBUkdFVF9FTlZ9IgplY2hvICItLT4gUmVxdWVzdCBJRCAgOiAke1JFUVVFU1RfSUR9IgplY2hvICItLT4gRm9yY2UgRmFpbCAgOiAke0ZPUkNFX0ZBSUx9IgplY2hvICItLT4gTm9kZSBOYW1lICAgOiAke05PREVfTkFNRTotYnVpbHQtaW59IgoKaWYgWyAiJHtGT1JDRV9GQUlMfSIgPSAidHJ1ZSIgXTsgdGhlbgogICAgZWNobyAiW0VSUk9SXSBTaW11bGF0ZWQgZmFpbHVyZSB0cmlnZ2VyZWQgdmlhIEZPUkNFX0ZBSUw9dHJ1ZSEiCiAgICBleGl0IDEKZmkKCmNhdCA8PCBKU09OX0VPRiA+IGF1ZGl0X3JlcG9ydC5qc29uCnsKICAicmVxdWVzdF9pZCI6ICIke1JFUVVFU1RfSUR9IiwKICAiZW52aXJvbm1lbnQiOiAiJHtUQVJHRVRfRU5WfSIsCiAgIndvcmtlcl9idWlsZCI6ICIke0JVSUxEX05VTUJFUn0iLAogICJleGVjdXRlZF9vbiI6ICIke05PREVfTkFNRTotYnVpbHQtaW59IiwKICAiY2hlY2tzX3Bhc3NlZCI6IHRydWUKfQpKU09OX0VPRgoKZWNobyAiW1NVQ0NFU1NdIGF1ZGl0X3JlcG9ydC5qc29uIGdlbmVyYXRlZCBpbiAke1dPUktTUEFDRX0iCg==".decodeBase64())
job.getBuildersList().clear()
job.getBuildersList().add(new Shell(decodedScript))

job.getPublishersList().clear()
def archiver = new ArtifactArchiver('audit_report.json')
archiver.setOnlyIfSuccessful(true)
job.getPublishersList().add(archiver)

job.save()
println "LESSON9_WORKER_READY"
