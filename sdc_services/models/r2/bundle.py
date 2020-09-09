def as_bundle(fhir_resources, bundle_type='collection'):
    entries = []
    for fhir_resource in fhir_resources:
        entries.append(fhir_resource)

    bundle_fhir = {
        "resourceType": 'Bundle',
        'entry': entries,
        'type': bundle_type,
    }
    return bundle_fhir
