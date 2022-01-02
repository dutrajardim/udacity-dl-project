/**
 * Implement Gatsby's Node APIs in this file.
 *
 * See: https://www.gatsbyjs.com/docs/node-apis/
 */
//

const NODE_TYPE = `OLAP`

const Minio = require('minio')
const parquet = require('parquetjs-lite')

exports.sourceNodes = async ({
    actions,
    createContentDigest,
    createNodeId,
    getNodesByType,
}, { s3, olapCubes, bucket }) => {
    const { createNode } = actions

    const s3Client = new Minio.Client({
        endPoint: s3.endpoint,
        accessKey: s3.key,
        secretKey: s3.secret
    })

    async function s3GetPaths(bucket, prefix) {
        return new Promise((resolve, reject) => {
            let objects = s3Client.listObjectsV2(bucket, prefix, true)
            let paths = []
            objects.on('data', object => paths.push(object.name))
            objects.on('end', _ => resolve(paths))
            objects.on('error', error => {
                console.log(error)
                reject(error)
            })
        })
    }

    async function s3GetObject(bucket, key) {
        return new Promise((resolve, reject) => {
            let bufferArray = []
            s3Client.getObject(bucket, key, (error, stream) => {
                if (error) reject(error)

                stream.on('data', buffer => bufferArray.push(buffer))
                stream.on('end', _ => resolve(Buffer.concat(bufferArray)))
                stream.on('error', error => reject(error))
            })
        })
    }

    for (const { name, s3Key } of olapCubes) {

        const nodeType = `${NODE_TYPE}${name}`
        try {
            let paths = await s3GetPaths(bucket, s3Key)
            for (const path of paths) {
                if (!path.endsWith('.parquet')) continue

                let fileBuffer = await s3GetObject(bucket, path)

                let reader = await parquet.ParquetReader.openBuffer(fileBuffer)
                let cursor = reader.getCursor()

                while (record = await cursor.next()) {
                    record.count = Number(record.count)
                    let recordString = JSON.stringify({ ...record, count: undefined })

                    createNode({
                        ...record,
                        id: createNodeId(`${NODE_TYPE}-${recordString}`),
                        parent: null,
                        children: [],
                        internal: {
                            type: nodeType,
                            contentDigest: createContentDigest(record)
                        }
                    })
                }
            }
        } catch (error) {
            console.log(error)
        }

    }


    return
}