// Connect to the Ethereum network using MetaMask's provider
const provider = new ethers.providers.Web3Provider(window.ethereum);
// const provider = new ethers.providers.JsonRpcProvider('https://rpc-mumbai.maticvigil.com');
// Create a contract instance
const contract = new ethers.Contract(courseOpeningContractAddress, courseOpeningContractABI, provider);


const web3 = new Web3(window.ethereum);


const Transaction = {
  async getEventDataFromTransactionHash(transactionHash, formattedEvent, inputs) {
    try {
      let res = await fetch("/api/contract/transaction_hash", {
        method: "POST",
        body: JSON.stringify({
          transactionHash,
          formattedEvent,
          inputs
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
        // Converting to JSON
        .then(response => response.json())
      return res
    } catch (error) {
      console.error(error);
      return error; // Rethrow the error to handle it at a higher level
    }
  },
  async sendTransaction(functionName, functionArguments, value = null) {
    try {
      // Request user's permission to connect to their MetaMask account
      await window.ethereum.enable();

      // Get the signer (user's Ethereum account)
      const signer = provider.getSigner();
      // Encode the transaction data
      const txData = contract.interface.encodeFunctionData(functionName, functionArguments);
      // Create the transaction object
      const tx = {
        to: courseOpeningContractAddress,
        data: txData,
        value: Number(value)
      };

      // Send the transaction and wait for the result
      const txResponse = await signer.sendTransaction(tx);
      console.log('Transaction sent:', txResponse);
      return {
        res: txResponse,
        success: true
      }
    } catch (error) {
      console.error('Error:', error);
      return {
        res: error,
        success: false
      }
    }
  }
}


function toggleForm(formId) {


  const forms = ["buyCourseForm", "fundContractForm", "withdrawContractForm",
    "openCourseForm", "viewDetailForm", "getTokenURIForm", "setMinterForm", "mintBatchForm", "getBoughtCourse", "addCourseForm"];
  forms.forEach(form => {
    console.log(form)
    console.log(document.getElementById(form))
    document.getElementById(form).style.display = "none";
  });
  console.log(formId)
  document.getElementById(formId).style.display = "block";
}

async function buyCourse() {
  const courseID = document.getElementById('courseID').value;
  let courseIDs = await contract.getAllCourseIDs()
  const functionName = 'buyCourse'; // Replace with the name of the function you want to call
  const functionArguments = [courseID]; // Replace with the arguments for the function
  showMessage(`Successfull buy <ul> <li>Course id: ${courseID}</li></ul>`)
  let result = await Transaction.sendTransaction(functionName, functionArguments, 20)
  if (!result.success) {
    console.log('invalid transaction')
    return;
  }
  const inputs = [
    { type: "string", name: "courseID" },
    { type: "address", name: "buyer", indexed: true },
    { type: "uint256", name: "value" },
    { type: "uint256", name: "tokenID" }
  ];
  showMessage(`Successfull buy <ul> <li>Course id: ${courseID}</li>
  <li>Buyer: ${buyer}</li>
  <li>Value: ${value}</li>
  <li>NFT TokenID  id: ${tokenID}</li></ul>`)
  setTimeout(async () => {
    console.log(result.res.hash)
    let eventDataForMint = await Transaction.getEventDataFromTransactionHash(result.res.hash, "CourseBought(string,address,uint256,uint256)", inputs)
    console.log(eventDataForMint)
    eventDataForMint = eventDataForMint.res
    showMessage(`Successfull buy <ul> <li>Course id: ${eventDataForMint.courseID}</li>
    <li>Value: ${eventDataForMint.value}</li>
    <li>NFT TokenID  id: ${eventDataForMint.tokenID}</li></ul>`)
    let res = await fetch("/api/contract/set_uri", {
      method: "POST",
      body: JSON.stringify({
        courseID,
        uri: `conft/${eventDataForMint.tokenID}`
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    })
    closeModal();
  }, 10000);

}

async function fundContract() {
  const amount = document.getElementById('amountFund').value;
  const functionName = 'fundContract'; // Replace with the name of the function you want to call
  const functionArguments = []; // Replace with the arguments for the function
  try {
    let result = await Transaction.sendTransaction(functionName, functionArguments, amount)
    console.log(result)
    if (result.success) showMessage(amount + " has been funded")

    else showMessage(result.res.data.message)

  } catch (err) {
    showMessage(err.data.message)
  }
  closeModal();
}


async function setMinter() {
  const addressOfMinter = document.getElementById('addressOfMinter').value;
  console.log('addressOfMinter:', addressOfMinter);

  const functionName = 'grantMinterRole'; // Replace with the name of the function you want to call
  const functionArguments = [addressOfMinter]; // Replace with the arguments for the function
  try {
    let result = await Transaction.sendTransaction(functionName, functionArguments)
    console.log(result)
    if (result.success)
      showMessage("Minter has set")

    else showMessage(result.res.data.message)
  } catch (err) {
    console.log(err)

  }
  closeModal();
}


async function getBoughtCourse() {
  let courseIDs = await contract.getAllCourseIDs()
  let courseBoughts = []
  const userAddress = window.ethereum.selectedAddress;
  for (let index = 0; index < courseIDs.length; index++) {
    const element = courseIDs[index];
    let isBought = await contract.ownsNFTForCourse(userAddress, element)
    if (isBought) courseBoughts.push(element)
  }
  console.log(courseBoughts)
  let html = courseBoughts.map(e => `<li>${e}</li>`)
  html = '<ul>' + html + '</ul>'
  showMessage("Courses: " + html)
  closeModal();
}


async function mintBatch() {
  const numberOfNFT = document.getElementById('numberOfNFT').value;
  const functionName = 'mintBatch'; // Replace with the name of the function you want to call
  const functionArguments = [numberOfNFT]; // Replace with the arguments for the function
  try {
    let result = await Transaction.sendTransaction(functionName, functionArguments)
    // console.log(result)
    // console.log(`konfauna`)
    if (result.success)
      showMessage(numberOfNFT + "  has been minted you can check it in your wallet")
    else showMessage(result.res.data.message)
  } catch (err) {
    console.log(err)
    showMessage(numberOfNFT + " has not yet been minted")

  }
  closeModal();
}

async function withdrawContract() {
  const amount = document.getElementById('amountWithdraw').value;

  const functionName = 'withDrawFunds'; // Replace with the name of the function you want to call
  const functionArguments = [amount]; // Replace with the arguments for the function
  try {
    let result = await Transaction.sendTransaction(functionName, functionArguments)
    if (result.success)
      showMessage(amount + " has been withdrawed")
    else showMessage(result.res.data.message)

  } catch (err) {
    console.log("heee", err)
    showMessage(amount + " has been not withdrawed")

  }

  console.log('Withdraw CourseOpening Contract:', amount);
  closeModal();
}

function openCourse() {
  const courseID = document.getElementById('courseIDOpen').value;
  window.location.href = `/course/view/${courseID}`;
  closeModal();
}

function earnCertificate() {
  const courseID = document.getElementById('courseIDEarn').value;
  window.location.href = `/course/earn_cert/${courseID}`;

  closeModal();
}

function viewCourseDetails() {
  const courseID = document.getElementById('courseIDDetail').value;
  console.log('View Course Details:', courseID);
  closeModal();
}

function getTokenURI() {
  const tokenID = document.getElementById('tokenID').value;
  let prefix =  'conft' 
  showMessage(`<a href='./metadata/${prefix}/${tokenID}'>TOKEN URI </a>`)
  console.log('Get Token URI:', tokenID, 'Opening Course NFT');
  closeModal();
}

async function AddCourse() {
  var form = document.getElementById('form_add_course');
  var formData = new FormData(form);

 let resultFromCourse = await fetch('/api/course/addcourse', {
    method: 'POST',
    body: formData
  }).then(response => response.json())
  const course = {
    courseID: resultFromCourse.course._id,
    price: resultFromCourse.course.price, // Example price in wei (1 ether)
  };
  console.log(course)
  const functionName = 'addCourse'; // Replace with the name of the function you want to call
  const functionArguments = [course]; // Replace with the arguments for the function
  let result = await Transaction.sendTransaction(functionName, functionArguments)
  if (!result.success) {
    console.log('invalid transaction')
    return;
  }
  showMessage(`Course's inserted with id: ${resultFromCourse.course._id}`)
  console.log('Get Token URI:', tokenID, 'Opening Course NFT:', openingCourseNFT, 'Certificate NFT:', certificateNFT);
  closeModal();
}



function closeModal() {
  // hideMessage()
  const modal = new bootstrap.Modal(document.getElementById('myModal'));
  console.log(modal)
  modal.hide();
}
function showMessage(courseID) {
  const successMessage = document.getElementById('successMessage');
  const successCourseID = document.getElementById('successCourseID');
  successCourseID.innerHTML = courseID;
  successMessage.classList.remove('d-none');
  setTimeout(() => {
    hideMessage();
  }, 30000); // Adjust the delay time in milliseconds (3 seconds in this example)
}


function hideMessage() {
  const successMessage = document.getElementById('successMessage');
  successMessage.classList.add('d-none');
}